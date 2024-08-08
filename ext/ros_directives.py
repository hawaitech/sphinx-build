"""Ros directives."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from docutils import nodes
from docutils.parsers.rst.directives import unchanged
from sphinx.util.docutils import SphinxDirective, SphinxRole

if TYPE_CHECKING:
    from sphinx.application import Sphinx

ros_pkg = {}
ros_exec = {}
ACT_PKG = None
ACT_EXEC = None


def create_table_row(title: str, *cases) -> nodes.Node:
    """Create a row within a table in the doc."""
    in_row = nodes.row()
    in_row.append(nodes.entry("", nodes.paragraph("", text=f"{title}")))
    for case in cases:
        in_row.append(nodes.entry("", nodes.paragraph("", text=f"{case}")))
    return in_row


class Param:
    """Parameters used in ros executables."""

    def __init__(self, name, param_type=None, default=None, description=None):
        self.name = name
        self.param_type = param_type
        self.default = default
        self.description = description

    def show(self):
        """Render a param."""
        param_descr = nodes.table()
        title_row = create_table_row("Type", "Default", "Description")
        value_row = create_table_row(self.param_type, self.default, self.description)
        param_descr.append(
            nodes.tgroup(
                "",
                nodes.colspec("", colwidth=2),
                nodes.colspec("", colwidth=2),
                nodes.colspec("", colwidth=2),
                nodes.tbody("", title_row, value_row),
            )
        )
        return param_descr


class Interface:
    """Describe an in and out interface."""

    def __init__(
        self,
        name,
        descr,
        category,
        in_type,
        in_descr,
        out_type,
        out_descr,
        status_type,
        status_descr,
    ):
        self.name = name
        self.category = category
        self.descr = descr
        self.in_type = in_type
        self.in_descr = in_descr
        self.out_type = out_type
        self.out_descr = out_descr
        self.status_type = status_type
        self.status_descr = status_descr

    def show(self):
        """Render the interface in the doc."""
        param_descr = nodes.table()
        title_row = create_table_row("", "Type", "Description")
        table_descr = nodes.tgroup("", nodes.colspec("", colwidth=3), nodes.colspec("", colwidth=3))
        table_content = nodes.tbody("", title_row)

        lines = self.get_description()
        for line in lines:
            table_descr.append(nodes.colspec("", colwidth=3))
            table_content.append(line)
        table_descr.append(table_content)
        param_descr.append(table_descr)
        return param_descr

    @abstractmethod
    def get_description(self):
        """Get description."""
        ...


class TopicIn(Interface):
    """Descrpiton class for topic in."""

    def get_description(self):
        """Return the line corresponding to the in parameter of the topic."""
        in_row = create_table_row(
            "In",
            self.in_type if self.in_type is not None else "-",
            self.in_descr if self.in_descr is not None else "-",
        )
        return [in_row]


class TopicOut(Interface):
    """Descrpiton class for topic out."""

    def get_description(self):
        """Return the line corresponding to the out parameter of the topic."""
        out_row = create_table_row(
            "Out",
            self.out_type if self.out_type is not None else "-",
            self.out_descr if self.out_descr is not None else "-",
        )
        return [out_row]


class Service(Interface):
    """Descrpiton class for service."""

    def get_description(self):
        """Return the line corresponding to the out parameter of the topic."""
        in_row = create_table_row(
            "In",
            self.in_type if self.in_type is not None else "-",
            self.in_descr if self.in_descr is not None else "-",
        )

        out_row = create_table_row(
            "Out",
            self.out_type if self.out_type is not None else "-",
            self.out_descr if self.out_descr is not None else "-",
        )
        return [in_row, out_row]


class Action(Interface):
    """Descrpiton class for action."""

    def get_description(self):
        """Return the line corresponding to the out parameter of the topic."""
        request_row = create_table_row(
            "Request",
            self.in_type if self.in_type is not None else "-",
            self.in_descr if self.in_descr is not None else "-",
        )

        result_row = create_table_row(
            "Result",
            self.out_type if self.out_type is not None else "-",
            self.out_descr if self.out_descr is not None else "-",
        )

        status_row = create_table_row(
            "Status",
            self.status_type if self.status_type is not None else "-",
            self.status_descr if self.status_descr is not None else "-",
        )
        return [request_row, result_row, status_row]


class RosExec:
    """Ros executable."""

    def __init__(self, name, loc=None, short_descr=None, long_descr=None):
        ros_exec[name] = self
        self.name = name
        self.loc = loc
        self.short_descr = (short_descr,)
        self.long_descr = long_descr
        self.params = []
        self.interfaces = []

    def add_param(self, name, param_type=None, default=None, description=None):
        """Add a parameter to an executable."""
        self.params.append(Param(name, param_type, default, description))

    def add_interface(
        self,
        name,
        descr,
        category,
        in_type,
        in_descr,
        out_type,
        out_descr,
        status_type,
        status_description,
    ):
        """Add an interface to an executable."""
        match category:
            case "service in":
                interface = Service
            case "service out":
                interface = Service
            case "topic in":
                interface = TopicIn
            case "topic out":
                interface = TopicOut
            case "action":
                interface = Action
            case _:
                raise NotImplementedError
        self.interfaces.append(
            interface(
                name,
                descr,
                category,
                in_type,
                in_descr,
                out_type,
                out_descr,
                status_type,
                status_description,
            )
        )

    def create_exemple_code(self):
        """Create the exemple parameter code."""
        code_block = nodes.literal_block(xml_space="preserved")
        exemple_config = f"{self.name}:\n   ros_parameters:\n      "
        for param in self.params:
            exemple_config += f"{param.name}: {param.default}\n   "
        code_block.append(nodes.inline(text=f"{exemple_config}"))
        return code_block

    def show(self):
        """Render the Ros executable in the doc."""
        root = nodes.section(ids=[f"exec_{self.name}"])
        title = nodes.title("", f"{self.name} [Executable]")
        root.append(title)
        descr = nodes.paragraph("", self.long_descr)
        root.append(descr)
        params_list_title = nodes.subtitle("", "Parameters description")
        root.append(params_list_title)
        params_list = nodes.field_list()
        for arg in self.params:
            params_list.append(
                nodes.field(
                    "", nodes.field_name("", f"{arg.name}"), nodes.field_body("", arg.show())
                )
            )
        root.append(params_list)
        exec_used_title = nodes.subtitle("", "Interfaces description")
        root.append(exec_used_title)
        interfaces_list = nodes.field_list()
        for interface in self.interfaces:
            interfaces_list.append(
                nodes.field(
                    "",
                    nodes.field_name("", f"{interface.name} [{interface.category}]"),
                    nodes.field_body("", interface.show()),
                )
            )
        root.append(interfaces_list)
        return root


class RosLaunch:
    """Ros launch."""

    def __init__(self, name, loc, short_descr, long_descr, exec_used=None):
        self.name = name
        self.loc = loc
        self.short_descr = (short_descr,)
        self.long_descr = long_descr
        self.args = []
        self.exec_used = exec_used if exec_used is not None else []

    def add_arg(self, name, param_type=None, default=None, description=None):
        """Add an argument to the launch file."""
        self.args.append(Param(name, param_type, default, description))

    def add_exec(self, exec_name):
        """Add an executable used in the launch file."""
        self.exec_used.append(ros_exec[exec_name])

    def show(self):
        """Render the launch file documentation."""
        root = nodes.section(ids=[f"launch_{self.name}"])
        title = nodes.title("", f"{self.name} [Launch file]")
        root.append(title)
        descr = nodes.paragraph("", self.long_descr)
        root.append(descr)
        args_list_title = nodes.subtitle("", "Arguments description")
        root.append(args_list_title)
        args_list = nodes.field_list()
        for arg in self.args:
            args_list.append(
                nodes.field(
                    "", nodes.field_name("", f"{arg.name}"), nodes.field_body("", arg.show())
                )
            )
        root.append(args_list)
        exec_used_title = nodes.subtitle("", "Executable used in launch file")
        root.append(exec_used_title)
        exec_list = nodes.bullet_list()
        for executable in self.exec_used:
            if executable in ros_exec:
                executable = ros_exec[executable]  # noqa: PLW2901, ok in this context
                exec_list.append(
                    nodes.list_item(
                        "", nodes.paragraph("", f"{executable.name}: {executable.short_descr[0]}")
                    )
                )
            else:
                exec_list.append(nodes.list_item("", nodes.paragraph("", f"{executable}")))
        root.append(exec_list)
        return root


class RosPackage:
    """Ros package."""

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self.executables = {}
        self.launch = {}

    def add_exec(self, exec_name, loc=None, short_descr="", long_descr=""):
        """Add an executable to the package."""
        self.executables[exec_name] = RosExec(
            name=exec_name, loc=loc, short_descr=short_descr, long_descr=long_descr
        )

    def add_launch(self, exec_name, loc=None, short_descr="", long_descr="", exec_used=None):
        """Add an executable to the package."""
        self.launch[exec_name] = RosLaunch(
            name=exec_name,
            loc=loc,
            short_descr=short_descr,
            long_descr=long_descr,
            exec_used=exec_used,
        )

    def show(self):
        """Render the package description in the documentation."""
        root = nodes.section(ids=[f"pkg_{self.name}"])
        title = nodes.title("", f"{self.name} [Ros package]", color="red")
        toc_list = nodes.bullet_list()
        toc_launch_list = nodes.bullet_list(bullet="-")
        toc_exec_list = nodes.bullet_list(bullet="-")
        descr = nodes.paragraph("", self.description)
        exec_list_title = nodes.subtitle("", "Executable files description")
        exec_list = nodes.paragraph()
        for executable in self.executables.values():
            toc_exec_list.append(
                nodes.list_item(
                    "",
                    nodes.paragraph(
                        "",
                        "",
                        nodes.reference(
                            "",
                            "",
                            nodes.paragraph(text=f"{executable.name}: {executable.short_descr[0]}"),
                            refid=f"exec_{executable.name}",
                        ),
                    ),
                )
            )
            exec_list.append(executable.show())
        launch_list_title = nodes.subtitle("", "Launch files description")
        launch_list = nodes.paragraph()
        for launch in self.launch.values():
            toc_launch_list.append(
                nodes.list_item(
                    "",
                    nodes.paragraph(
                        "",
                        "",
                        nodes.reference(
                            "",
                            "",
                            nodes.paragraph(text=f"{launch.name}: {launch.short_descr[0]}"),
                            refid=f"launch_{launch.name}",
                        ),
                    ),
                )
            )
            launch_list.append(launch.show())
        toc_list.append(toc_exec_list)
        toc_list.append(toc_launch_list)
        root.append(title)
        root.append(descr)
        root.append(nodes.subtitle("", "Table of content"))
        root.append(toc_list)
        root.append(exec_list_title)
        root.append(exec_list)
        root.append(launch_list_title)
        root.append(launch_list)
        return root


class DeclarePackage(SphinxDirective):
    """Sphinx directive to declare a ros package."""

    required_arguments = 1
    option_spec = {"description": unchanged}

    def run(self) -> list[nodes.Node]:
        """Create a pck in global variables."""
        global ACT_PKG
        ACT_PKG = self.arguments[0]
        ros_pkg[self.arguments[0]] = RosPackage(
            name=self.arguments[0], description=self.options["description"]
        )
        return []


class EndPackage(SphinxDirective):
    """Sphinx directive to declare a ros package."""

    def run(self) -> list[nodes.Node]:
        """End the description of the current package."""
        global ACT_PKG
        ACT_PKG = None
        return []


class DeclareExec(SphinxDirective):
    """Declare a new executable in the current package."""

    required_arguments = 1
    option_spec = {"short_descr": unchanged, "long_descr": unchanged}

    def run(self) -> list[nodes.Node]:
        """Declare an executable."""
        global ACT_EXEC
        ACT_EXEC = self.arguments[0]
        ros_pkg[ACT_PKG].add_exec(
            exec_name=ACT_EXEC,
            short_descr=self.options["short_descr"],
            long_descr=self.options["long_descr"],
        )
        return []


class EndExec(SphinxDirective):
    """Sphinx directive to declare a ros package."""

    def run(self) -> list[nodes.Node]:
        """End the current executable description."""
        global ACT_EXEC
        ACT_EXEC = None
        return []


class DeclareParam(SphinxDirective):
    """A directive to describe a parameter of an executable."""

    required_arguments = 1
    option_spec = {"type": unchanged, "default": unchanged, "description": unchanged}

    def run(self) -> list[nodes.Node]:
        """Declare a parameter in the current context, should be executable."""
        ros_pkg[ACT_PKG].executables[ACT_EXEC].add_param(
            name=self.arguments[0],
            param_type=self.options["type"],
            default=self.options["default"],
            description=self.options["description"],
        )
        return []


class DeclareInterface(SphinxDirective):
    """A directive to add an interface into an executable."""

    required_arguments = 1
    option_spec = {
        "description": unchanged,
        "category": unchanged,
        "in_type": unchanged,
        "in_description": unchanged,
        "out_type": unchanged,
        "out_description": unchanged,
        "status_type": unchanged,
        "status_description": unchanged,
    }

    def run(self) -> list[nodes.Node]:
        """Declare an interface in the current context."""
        for option in self.option_spec:
            if option not in self.options:
                self.options[option] = None
        ros_exec[ACT_EXEC].add_interface(
            self.arguments[0],
            self.options["description"],
            self.options["category"],
            self.options["in_type"],
            self.options["in_description"],
            self.options["out_type"],
            self.options["out_description"],
            self.options["status_type"],
            self.options["status_description"],
        )
        return []


def str_option_to_list(options: str) -> list[str]:
    """Convert a list of option separate by, into a list of option str."""
    return [x.replace(" ", "") for x in options.split(",")]


class DeclareLaunch(SphinxDirective):
    """Declare a new launch in the current package."""

    required_arguments = 1
    option_spec = {
        "short_descr": unchanged,
        "long_descr": unchanged,
        "exec_used": str_option_to_list,
    }

    def run(self) -> list[nodes.Node]:
        """Declare a new launch file."""
        global ACT_EXEC
        ACT_EXEC = self.arguments[0]
        ros_pkg[ACT_PKG].add_launch(
            exec_name=ACT_EXEC,
            short_descr=self.options["short_descr"],
            long_descr=self.options["long_descr"],
            exec_used=self.options["exec_used"],
        )
        return []


class DeclareArg(SphinxDirective):
    """A directive to describe a parameter of an executable."""

    required_arguments = 1
    option_spec = {"type": unchanged, "default": unchanged, "description": unchanged}

    def run(self) -> list[nodes.Node]:
        """Declare a new argument in the context, should be launch file."""
        ros_pkg[ACT_PKG].launch[ACT_EXEC].add_arg(
            name=self.arguments[0],
            param_type=self.options["type"],
            default=self.options["default"],
            description=self.options["description"],
        )
        return []


class ShowPacakage(SphinxDirective):
    """Write description of a ros pacakge."""

    required_arguments = 1

    def run(self) -> list[nodes.Node]:
        """Render the package description."""
        pkg: RosPackage
        pkg = ros_pkg[self.arguments[0]]
        return [pkg.show()]


class RefPackage(SphinxRole):
    """A role to reference a ros package."""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        """Render a reference to ros package."""
        node = nodes.inline("", "", nodes.reference("", f"{self.text}", refid=f"pkg_{self.text}"))
        return [node], []


class RefExec(SphinxRole):
    """A role to reference a ros executable."""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        """Render a reference to ros executable."""
        node = nodes.inline("", "", nodes.reference("", f"{self.text}", refid=f"exec_{self.text}"))
        return [node], []


class RefLaunch(SphinxRole):
    """A role to reference a ros launch file."""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        """Render a reference to ros launch."""
        node = nodes.inline(
            "", "", nodes.reference("", f"{self.text}", refid=f"launch_{self.text}")
        )
        return [node], []


def setup(app: Sphinx) -> dict:
    """Declare new roles and directives usable in doc rst files."""
    app.add_directive("declare_ros_parameter", DeclareParam)
    app.add_directive("declare_ros_arg", DeclareArg)
    app.add_directive("declare_ros_interface", DeclareInterface)
    app.add_directive("begin_ros_pkg", DeclarePackage)
    app.add_directive("begin_ros_exec", DeclareExec)
    app.add_directive("begin_ros_launch", DeclareLaunch)
    app.add_directive("end_ros_pkg", EndPackage)
    app.add_directive("end_ros_exec", EndExec)
    app.add_directive("end_ros_launch", EndExec)
    app.add_directive("show_ros_pkg", ShowPacakage)

    app.add_role("ref_ros_pkg", RefPackage())
    app.add_role("ref_ros_exec", RefExec())
    app.add_role("ref_ros_launch", RefLaunch())
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
