# Directives

## begin_ros_pkg

Start the documentation of a new ros package.

### Arguments

* package_name: The package name.

### Options

* description: Description of the package.

## end_ros_pkg

End the documentation of current ros package.

## begin_ros_exec

Start the documentation of a new ros executable.

### Arguments

* exec_name: The executable name.

### Options

* short_descr: One line description of the executable.
* long_descr: multi-line description of the executable.

## end_ros_exec

End the documentation of current ros executable.

## begin_ros_launch

Start the documentation of a new ros launch file.

### Arguments

* elaunch_name: The launch file name.

### Options

* short_descr: One line description of the launch file.
* long_descr: Multi-line description of the launch file.
* exec_used: A coma separated list of all executable used in the launch file.

## end_ros_launch

End the documentation of current ros launch file.

## declare_ros_parameter

Declare a new parameter for the current ros executable.

## Arguments

* param_name: the parameter name

### Options

* type: The type of the parameter.
* default: Defulat value for this parameter.
* description: The description of the parameter.

## declare_ros_arg

Declare a new arguments for the current ros launch file.

## Arguments

* arg_name: the argument name

### Options

* type: The type of the argument.
* default: Defulat value for this argument.
* description: The description of the argument.

## declare_ros_interface

Declare a new interface for the current ros executable. According to the category of your interface you only need some of the options.

## Arguments

* param_name: the parameter name.

### Options

* description: The description of the interface.
* category: The category of the interface (topic_in, topic_out, services, actions)
* in_type: The type of the input.
* in_description: The description of the input.
* out_type: The type of the output.
* out_description: The description of the output.
* status_type: The type of the status.
* status_description: The description of the status.

## show_ros_pkg

Render the package within the website documentation.

## Arguments

* package_name: The package name to render.

# Roles

## ref_ros_pkg

Create a reference to a ros package.

### Arguments

* pkg_name: the package name to refer.

## ref_ros_exec

Create a reference to a ros executable.

### Arguments

* exec_name: the executable name to refer.

## ref_ros_launch

Create a reference to a ros launch file.

### Arguments

* launch_name: the launch file name to refer.