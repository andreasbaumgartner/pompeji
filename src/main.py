import json
import inquirer
import os
import sys
from argparse import ArgumentParser
from rich.console import Console


class Application:
    """Main class to handle the application logic."""

    @staticmethod
    def main():
        # base workflow
        # ------------ #
        msg = Messages()
        msg.welcome_msg()
        args = CommandParser()
        option = args.get_option()
        project_name = option.project_name

        # templates
        # ------------ #
        # show user templates
        template = Template()
        templates = template.get_templates()
        question = BaseQuestion()
        s_template = question.multiple_choice_questions(
            choices=templates,
            message="Which Plugin you want do use?",
        )
        # print the selected template
        msg.warning_msg(f"Selected Template: {s_template}")

        # selected plugin
        template.read_template("base.json")

        # convert the plugin into actions
        result = template.convert_template()
        msg.success_msg(result)

        msg.success_msg(f"Base: {template.base_files}")

        # process the service for the base files
        struct = BaseStructureGenerator()
        struct.create_dir()
        struct.return_project_dir()

        # basic generation
        # ------------ #
        # generator = BaseStructureGenerator(project_name)
        # generator.create_dir()
        # generator.create_subdirs()
        # file_generator = BaseFileGenerator(project_name)
        # file_generator.create_base_files()
        # service = BaseService()
        # service.ask_service()
        # service.create_service()
        # TEST: Test with the template class

        print(f"Project structure for '{project_name}' created successfully.")


class Messages:
    """Welcome message class."""

    def __init__(self):
        self.message = "Welcome to the Python project generator tool 🚀"
        self.console = Console()

    def welcome_msg(self):
        """Display welcome message."""
        self.console.print("#" * 48, style="bold blue")
        self.console.print(self.message, style="bold blue")
        self.console.print("#" * 48, style="bold blue")

    def error_msg(self, message: str = "An Error"):
        """Display error message."""
        self.console.print({message}, style="bold red")

    def warning_msg(self, message: str = "A Warning"):
        """Display warning message."""
        self.console.print(message, style="bold yellow")

    def success_msg(self, message: str = "Success"):
        """Display success message."""
        self.console.print(message, style="bold green")

    def notice_msg(self):
        """Display notice message."""
        self.console.print("A notice occurred", style="bold green")

    def print_msg(self):
        """Print message."""
        self.console.print(self.message)


class CommandParser:
    """Parse command line arguments."""

    def __init__(self):
        self.args = sys.argv[1:]
        self.option = None

    def get_option(self):
        """Get the option."""
        arg_parser = ArgumentParser()
        arg_parser.add_argument(
            "-o",
            "--option",
            type=str,
            help="Specify an option",
        )
        arg_parser.add_argument(
            "project_name",
            type=str,
            help="Specify the project name",
        )
        arg_parser.add_argument(
            "-s",
            "--service",
            type=str,
            help="Specify a service",
        )
        arg_parser.add_argument(
            "-t",
            "--template",
            type=str,
            help="Specify a template",
        )
        arg_parser.add_argument(
            "-c",
            "--config",
            type=str,
            help="Specify a configuration file",
        )
        args = arg_parser.parse_args()

        return args


class BaseStructureGenerator:
    """Create basic file structure for a project."""

    def __init__(self, project_name):
        self.project_name = project_name
        self.current_path = os.getcwd()
        self.err_message_exists = "Project already exists / cd into the project"  # noqa: E501
        self.req_dir = "requirements"

    def create_dir(self):
        """Create project directories."""
        path_to_create = os.path.join(self.current_path, self.project_name)
        try:
            os.makedirs(path_to_create, exist_ok=False)
        except FileExistsError:
            print(self.err_message_exists)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

    def create_subdirs(self):
        """Create subdirectories."""
        os.makedirs(os.path.join(self.current_path, self.project_name, self.req_dir))  # noqa: E501

    def return_project_dir(self):
        """Return the project directory."""
        return os.path.join(self.current_path, self.project_name)


class BaseFileGenerator:
    """Create basic files for a project."""

    def __init__(self, project_name):
        self.project_name = project_name
        self.current_path = os.getcwd()
        self.base_files = [
            ".gitignore",
            "README.md",
            "main.py",
        ]
        self.subdir_files = [
            "dev_requirements.txt",
            "requirements.txt",
        ]
        self.subdir = "requirements"

    def create_base_files(self):
        """Create base files for a project."""
        for file in self.base_files:
            open(os.path.join(self.current_path, self.project_name, file), "w").close()  # noqa: E501

    def create_subdir_files(self):
        """Create files in subdirectories."""
        for file in self.subdir_files:
            open(
                os.path.join(self.current_path, self.project_name, self.subdir, file),  # noqa: E501
                "w",
            ).close()


class BaseQuestion:
    """Base question service class."""

    def __init__(self):
        self.questions = []
        self.choices = []
        self.message = ""
        self.default = ""

    def choice_questions(
        self, choices: list[str], message: str, default: str
    ) -> dict[str, str] | None:
        """Ask choice questions."""
        questions = [
            inquirer.List(
                "choice",
                message=message,
                choices=choices,
                default=default,
            )
        ]
        return inquirer.prompt(questions)

    def multiple_choice_questions(
        self, choices: list[str], message: str, default: str = None
    ) -> dict[str, str] | None:
        """Ask multiple choice questions."""
        if default is not None:
            questions = [
                inquirer.Checkbox(
                    "choice",
                    message=message,
                    choices=choices,
                    default=default,
                )
            ]
            return inquirer.prompt(questions)
        else:
            questions = [
                inquirer.Checkbox(
                    "choice",
                    message=message,
                    choices=choices,
                )
            ]
            return inquirer.prompt(questions)


class BaseService:
    """Base service class."""

    def __init__(self):
        self.current_path = os.getcwd()
        self.project_name = sys.argv[1]
        self.question = BaseQuestion()
        self.service = None
        self.message = ""
        self.services = [
            "git",
            "github",
            "virtualenv",
            "pytest",
            "LICENSE",
            "setup.cfg",
            "setup.nox",
        ]
        self.defaults = ["git", "readme"]

    def ask_service(self):
        """Create service."""
        self.service = self.question.multiple_choice_questions(
            self.services, "Select a service", self.defaults
        )
        return self.service

    def create_service(self) -> str | None:
        """Create service."""
        if self.service is not None:
            for choice in self.service["choice"]:
                if choice == "git":
                    self.create_git_repository()
                elif choice == "github":
                    self.create_github_repository()
                elif choice == "pytest":
                    self.create_pytest()
                elif choice == "LICENSE":
                    self.create_license()
                elif choice == "setup.cfg":
                    self.create_setup_cfg()
                elif choice == "setup.nox":
                    self.create_setup_nox()
                elif choice == "virtualenv":
                    self.create_virtual_environment()
        else:
            print("No service selected")

    def create_virtual_environment(self):
        """Create virtual environment."""
        os.system(f"cd {self.project_name} && python3 -m venv venv")
        return print("Virtual environment created")

    def create_git_repository(self) -> str:
        """Create git repository."""
        os.system(f"cd {self.project_name} && git init")
        return "Git repository created"

    def create_github_repository(self):
        """Create github repository."""
        print("Not supported yet")
        return sys.exit(1)

    # TODO: to install package inside the join another process
    def create_pytest(self):
        """Create pytest."""
        print("Not implemented yet")
        return "Pytest created"

    def create_license(self) -> str:
        """Create LICENSE File."""
        open(os.path.join(self.current_path, self.project_name, "LICENSE"), "a").close()  # noqa: E501
        return "License created"

    def create_setup_cfg(self):
        """Create setup.cfg."""
        print("Not implemented yet")
        return sys.exit(1)

    def create_setup_nox(self):
        """Create setup.nox."""
        print("Not implemented yet")
        return sys.exit(1)


class Template:
    """Base class for templates."""

    def __init__(self):
        self.template_path = os.path.join(os.getcwd(), "templates")
        self.templates = []
        self.template = None
        self.base_files = []
        self.services = []
        self.python_version = None
        self.config = None

    def get_templates(self):
        """Return all available templates."""
        self.templates = os.listdir(self.template_path)
        return self.templates

    def read_template(self, file_name):
        """Read the template file"""
        with open(os.path.join(self.template_path, file_name), "r") as file:
            self.template = file.read()
            return self.template

    def convert_template(self) -> str:
        """Convert a selected .json template"""
        if self.template is not None:
            data = json.loads(self.template)

            self.base_files = data["base"]
            self.services = data["services"]
            self.python_version = data["python"]
            self.config = data["config"]

            return (self.base_files, self.services, self.python_version, self.config)


if __name__ == "__main__":
    Application.main()
