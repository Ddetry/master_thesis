import os
import json
import importlib

from tkinter import messagebox, ttk

import thonny

from thonny import get_runner, get_workbench
from thonny.common import InlineCommand
from thonny.languages import tr
from thonny.memory import VariablesFrame
from thonny import ast_utils, get_workbench, ui_utils, get_runner

from thonny import THONNY_USER_DIR, common, get_runner, get_shell, get_workbench
from thonny.common import (
    BackendEvent,
    CommandToBackend,
    DebuggerCommand,
    DebuggerResponse,
    EOFCommand,
    InlineCommand,
    InputSubmission,
    ToplevelCommand,
    ToplevelResponse,
    UserError,
    is_same_path,
    normpath_with_actual_case,
    parse_message,
    path_startswith,
    serialize_message,
    update_system_path,
    MessageFromBackend,
    universal_relpath,
)
from thonny.editors import (
    get_current_breakpoints,
    get_saved_current_script_filename,
    is_remote_path,
    is_local_path,
    get_target_dirname_from_editor_filename,
    extract_target_path,
)

from thonny.misc_utils import construct_cmd_line, running_on_mac_os, running_on_windows
from thonny.ui_utils import CommonDialogEx, select_sequence, show_dialog
from thonny.workdlg import WorkDialog


class VariablesView(VariablesFrame):
    def __init__(self, master):
        super().__init__(master)

        ttk.Style().configure("Centered.TButton", justify="center")
        self.back_button = ttk.Button(
            self.tree,
            style="Centered.TButton",
            text=tr("Back to\ncurrent frame"),
            command=self._handle_back_button,
            width=15,
        )

        get_workbench().bind("BackendRestart", self._handle_backend_restart, True)
        get_workbench().bind("ToplevelResponse", self._handle_toplevel_response, True)
        # get_workbench().bind("DebuggerResponse", self._debugger_response, True)
        get_workbench().bind("get_frame_info_response", self._handle_frame_info_event, True)
        get_workbench().bind("get_globals_response", self._handle_get_globals_response, True)

        self.globals_vars = None

        # records last info from progress messages
        self._last_active_info = None

    # remove the variable all_vars from the globals variables
    def remove_all_vars(self):
        for i in range(0, len(self.globals_vars) - 1):
            if (self.globals_vars[i][0] == "all_vars"):
                del (self.globals_vars[i])


    def get_all_globals_variables(self):
        filename = get_saved_current_script_filename()
        print(filename)
        data = data2 = ""
        with open(filename) as fp:
            data = fp.read()

        filepath = os.getcwd() 
        filepath += "/thonny/plugins/texte.py"

        with open(filepath) as fp:
            data2 = fp.read()
        data += "\n"
        data += data2

        with open ('temp.py', 'w') as fp:
            fp.write(data)

        fp.close()

        import temp 
        importlib.reload(temp)
        temp.myloop()
        temp.all_vars.pop(0)

        for x in range(0, len(temp.all_vars)-1):
            if temp.all_vars[x][0] == "all_variables":
                temp.all_vars.pop(x)
        
        get_workbench().event_generate("Fill_global", myglobal=temp.all_vars)
        self.globals_vars = temp.all_vars


    #modif
    def on_double_click(self, event):
        self.show_object_info()

    def show_object_info(self):
        object_id = self.get_object_id()
        get_workbench().event_generate("GetAllObjectInfo", id=object_id)

        if object_id is None:
            return

        iid = self.tree.focus()
        if not iid:
            return

        name_of_var = self.tree.item(iid)["values"][0]

        if(self.globals_vars != None):
            for i in range(0, len(self.globals_vars)-1):
                if(self.globals_vars[i][0] == name_of_var):
                    get_workbench().event_generate("ActiveGraphView", object=self.globals_vars[i])
                    return

    def get_id_with_name(self):
        for i in range(0, len(self.globals_vars) - 1):
            if (self.globals_vars[i][0] ):
                get_workbench().event_generate("ActiveGraphView", object=self.globals_vars[i])
                return


    def _update_back_button(self, visible):
        if visible:
            assert self._last_active_info is not None
            self.back_button.configure(text=tr("Back to\n%s") % self._last_active_info[-1])
            self.back_button.place(relx=1, x=-5, y=5, anchor="ne")
        else:
            self.back_button.place_forget()

    def _handle_back_button(self):
        assert self._last_active_info is not None
        if len(self._last_active_info) == 2:
            self.show_globals(*self._last_active_info)
        else:
            assert len(self._last_active_info) == 4
            self.show_frame_variables(*self._last_active_info)

    def _handle_backend_restart(self, event):
        self._clear_tree()
        self.get_all_globals_variables()

    def _handle_get_globals_response(self, event):
        if "error" in event:
            self._clear_tree()
            messagebox.showerror("Error querying global variables", event["error"], master=self)
        elif "globals" not in event:
            self._clear_tree()
            messagebox.showerror("Error querying global variables", str(event), master=self)
        else:
            self.show_globals(event["globals"], event["module_name"])

    def _handle_toplevel_response(self, event):
        if "globals" in event:
            self.show_globals(event["globals"], "__main__")
        else:
            # MicroPython
            get_runner().send_command(InlineCommand("get_globals", module_name="__main__"))


    def show_globals(self, globals_, module_name, is_active=True):

        # modif
        self.from_globals_to_MyVar(globals_)

        # TODO: update only if something has changed
        self.update_variables(globals_)

        if module_name == "__main__":
            self._set_tab_caption(tr("Variables"))
        else:
            self._set_tab_caption(tr("Variables") + " (%s)" % module_name)

        if is_active:
            self._last_active_info = (globals_, module_name)

        self._update_back_button(not is_active)

    #modif
    def from_globals_to_MyVar(self, myglobals):
        myVar = []
        for name, val in myglobals.items():
            myVar.append((name, val[0], thonny.memory.format_object_id(val[0])))
        get_workbench().event_generate("Fill_myVar", var=myVar)


    def show_frame_variables(self, locals_, globals_, freevars, frame_name, is_active=True):
        # TODO: update only if something has changed
        actual_locals = {}
        nonlocals = {}
        for name in locals_:
            if name in freevars:
                nonlocals[name] = locals_[name]
            else:
                actual_locals[name] = locals_[name]

        groups = [("LOCALS", actual_locals), ("GLOBALS", globals_)]
        if nonlocals:
            groups.insert(1, ("NONLOCALS", nonlocals))

        self.update_variables(groups)
        self._set_tab_caption("Variables (%s)" % frame_name)

        if is_active:
            self._last_active_info = (locals_, globals_, freevars, frame_name)

        self._update_back_button(not is_active)

    def _handle_frame_info_event(self, frame_info):
        if frame_info.get("error"):
            "probably non-existent frame"
            return
        else:
            is_active = frame_info[
                "location"
            ] == "stack" or (  # same __main__ globals can be in different frames
                frame_info["code_name"] == "<module>"
                and frame_info["module_name"] == "__main__"
                and self._last_active_info[-1] == "__main__"
                and self._last_active_info[0] == frame_info["globals"]
            )

            if frame_info["code_name"] == "<module>":
                self.show_globals(frame_info["globals"], frame_info["module_name"], is_active)
            else:
                self.show_frame_variables(
                    frame_info["locals"],
                    frame_info["globals"],
                    frame_info["freevars"],
                    frame_info["code_name"],
                    is_active,
                )

    def _set_tab_caption(self, text):
        # pylint: disable=no-member
        if self.hidden:
            return

        self.home_widget.master.tab(self.home_widget, text=text)


def load_plugin() -> None:
    get_workbench().add_view(VariablesView, tr("Variables"), "ne", default_position_key="AAA")
