import json
import os
import sys
from argparse import ArgumentParser

import inquirer
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

        # ask user for manual or template
        # ------------ #
        question = BaseQuestion()
        process_qs = question.choice_questions(
            choices=["Manual", "Template"],
            message="Do you want to create a project manually or use a template?",  # noqa: E501
            default="Manual",
        )

        if process_qs["choice"] == "Template":
            # templates
            # ------------ #
            # show user templates
            template = Template()
            templates = template.get_templates()
            question = BaseQuestion()
            s_template = question.multiple_choice_questions(
                choices=templates,
                message="Which Template you wana use?",
            )
            # print the selected template
            try:
                msg.warning_msg(f"Selected Template: {s_template['choice'][0]}")  # noqa: E501

            except KeyError:
                msg.error_msg("No template selected")
                sys.exit(1)

            except IndexError:
                msg.error_msg("No template selected")
                sys.exit(1)

            # selected plugin
            # TODO:Check if it not None
            template.read_template(s_template["choice"][0])

            # convert the plugin into actions
            result = template.convert_template()
            msg.success_msg(result)

            msg.success_msg(f"Base: {template.base_files}")

            # process the service for the base files

            struct = BaseStructureGenerator(project_name)
            struct.create_dir()
            project_path = struct.return_project_dir()

            file = FileService(project_path)
            file.create_file(template.base_files)
            file.create_file_with_subdir(template.subdir)

            # services
            # ------------ #
            service = BaseService()
            need_config = service.run_service(template.services)

            # config
            # ------------ #
            config = Config()
            config.read_config(need_config)
            config.write_config(project_path)

        elif process_qs["choice"] == "Manual":
            # basic generation
            # ------------ #
            generator = BaseStructureGenerator(project_name)
            generator.create_dir()
            generator.create_subdirs()
            file_generator = BaseFileGenerator(project_name)
            file_generator.create_base_files()
            service = BaseService()
            service.ask_service()
            need_config = service.create_service()

        else:
            msg.error_msg("No option selected")
            sys.exit(1)


class Messages:
    """Welcome message class."""

    def __init__(self):
        self.message = "🚀 Welcome to the Python project generator tool 🚀"
        self.console = Console()

    def welcome_msg(self):
        """Display welcome message."""
        self.console.print("#" * 50, style="bold blue")
        self.console.print(self.message, style="bold blue")
        self.console.print("#" * 50, style="bold blue")

    def error_msg(self, message: str = "An Error"):
        """Display error message."""
        self.console.print(message, style="bold red")

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
        self.need_config = []

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
                    self.need_config.append("pytest")
                elif choice == "LICENSE":
                    self.create_license()
                elif choice == "setup.cfg":
                    self.create_setup_cfg()
                elif choice == "setup.nox":
                    self.create_setup_nox()
                    self.need_config.append("nox")
                elif choice == "virtualenv":
                    self.create_virtual_environment()
        else:
            print("No service selected")

        return self.need_config

    def run_service(self, services: list[str]) -> str:
        """Run service from a given list. Only for supported services."""
        for service in services:
            if service in self.services:
                if service == "git":
                    self.create_git_repository()
                elif service == "github":
                    self.create_github_repository()
                elif service == "pytest":
                    self.create_pytest()
                    self.need_config.append("pytest")
                elif service == "LICENSE":
                    self.create_license()
                elif service == "setup.cfg":
                    self.create_setup_cfg()
                elif service == "setup.nox":
                    self.create_setup_nox()
                    self.need_config.append("nox")
                elif service == "virtualenv":
                    self.create_virtual_environment()
            else:
                print(f"Service {service} not supported yet")

        return self.need_config

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


class FileService(Messages):
    """Class to create file as a service"""

    def __init__(self, project_path: str):
        self.services = []
        self.project_path = project_path
        self.req_dir = "requirements"

    def create_file(self, files):
        """create file based on the files provided"""
        for file in files:
            open(os.path.join(self.project_path, file), "w").close()  # noqa: E501
            self.services.append(file)

    def create_file_with_subdir(self, files):
        """create file with subdir necessary"""

        for file in files:
            if "requirements" in file:
                os.makedirs(
                    os.path.join(self.project_path, self.req_dir),
                    exist_ok=True,
                )
                open(os.path.join(self.project_path, self.req_dir, file), "w").close()  # noqa: E501
                self.services.append(file)
            else:
                Messages.error_msg("File for Subdir not supported")


class Template:
    """Base class for templates."""

    def __init__(self):
        self.template_path = os.path.join(os.getcwd(), "templates")
        self.templates = []
        self.template = None
        self.base_files = []
        self.subdir = []
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
            self.base_files = data["files"]
            self.subdir = data["subdir_files"]
            self.services = data["services"]
            self.config = data["config"]

            return (
                self.base_files,
                self.subdir,
                self.services,
                self.config,
            )


class Config:
    """Configuration class."""

    def __init__(self):
        self.configs = []

    def read_config(self, configs: list[str]):
        """Read the configuration and store it in a .json file."""
        for config in configs:
            self.configs.append(config)

    def write_config(self, project_path: str = None):
        """Write the configuration to a .json file."""
        for line in self.configs:
            if line == "pytest":
                # write to project path pyproject.toml
                with open(os.path.join(project_path, "pyproject.toml"), "w") as file:  # noqa: E501
                    # TODO: add example pytest config
                    file.write("[tool.pytest.ini_options]\naddopts = '-v'\n")
                    file.write("TestConifg = 'pytest.ini'")
                    file.close()

            elif line == "nox":
                print("Not implemented yet")


if __name__ == "__main__":
    Application.main()
