import inquirer
import os
import sys


class Application:
    """Main class to handle the application logic."""

    @staticmethod
    def main():
        if len(sys.argv) < 2:
            print("Please provide an argument like: 'project_name'")
            sys.exit(1)
        project_name = sys.argv[1]
        generator = BaseStructureGenerator(project_name)
        generator.create_dir()
        generator.create_subdirs()
        file_generator = BaseFileGenerator(project_name)
        file_generator.create_base_files()
        service = BaseService()
        service.ask_service()
        service.create_service()
        print(f"Project structure for '{project_name}' created successfully.")


class BaseStructureGenerator:
    """Create basic file structure for a project."""

    def __init__(self, project_name):
        self.project_name = project_name
        self.current_path = os.getcwd()
        self.err_message_exists = "Project already exists / cd into the project"
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
        os.makedirs(os.path.join(self.current_path, self.project_name, self.req_dir))

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
            open(os.path.join(self.current_path, self.project_name, file), "w").close()

    def create_subdir_files(self):
        """Create files in subdirectories."""
        for file in self.subdir_files:
            open(
                os.path.join(self.current_path, self.project_name, self.subdir, file),
                "w",
            ).close()


class BaseQuestion:
    """Base question service class."""

    def __init__(self):
        self.questions = []
        self.choices = []
        self.message = ""
        self.default = ""
        self.default_choices = []

    def multiple_choice_questions(
        self, choices: list[str], message: str, default: list[str]
    ) -> dict[str, str] | None:
        """Ask multiple choice questions."""
        questions = [
            inquirer.Checkbox(
                "choice",
                message=message,
                choices=choices,
                default=default,
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
        open(os.path.join(self.current_path, self.project_name, "LICENSE"), "a").close()
        return "License created"

    def create_setup_cfg(self):
        """Create setup.cfg."""
        print("Not implemented yet")
        return sys.exit(1)

    def create_setup_nox(self):
        """Create setup.nox."""
        print("Not implemented yet")
        return sys.exit(1)


if __name__ == "__main__":
    Application.main()
