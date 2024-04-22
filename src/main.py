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
        os.makedirs(os.path.join(self.current_path,
                    self.project_name, self.req_dir))

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
            "LICENSE",
            "setup.py",
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
            open(os.path.join(self.current_path,
                 self.project_name, file), "w").close()

    def create_subdir_files(self):
        """Create files in subdirectories."""
        for file in self.subdir_files:
            open(
                os.path.join(self.current_path, self.project_name,
                             self.subdir, file),
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
        self, choices: list[str], message: str, default: str
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
            "pytest",
            "readme",
            "license",
            "setup.cfg",
            "setup.nox",
        ]

    def ask_service(self):
        """Create service."""
        self.service = self.question.choice_questions(
            self.services, "Select a service", "git"
        )
        return self.service

    def create_service(self):
        """Create service."""
        if self.service == "git":
            self.message = self.create_git_repository()
        elif self.service == "github":
            self.create_github_repository()
        elif self.service == "pytest":
            self.create_pytest()
        elif self.service == "readme":
            self.create_readme()
        elif self.service == "license":
            self.create_license()
        elif self.service == "setup.cfg":
            self.create_setup_cfg()
        elif self.service == "setup.nox":
            self.create_setup_nox()

    def create_git_repository(self) -> str:
        """Create git repository."""
        os.system(f"cd {self.project_name} && git init")
        return "Git repository created"

    def create_github_repository(self):
        """Create github repository."""
        print("Not supported yet")
        return sys.exit(1)

    def create_pytest(self):
        """Create pytest."""
        print("Do you want to use pytest? (y/n)")
        c_pytest = input()
        if c_pytest == "y" or "yes":
            os.system(f"cd {self.project_name} && pip install -U pytest")
            print("Pytest installed")
        else:
            print("Pytest will not be installed")

    def create_readme(self):
        """Create readme."""
        print("Not implemented yet")
        return sys.exit(1)

    def create_license(self):
        """Create license."""
        print("Not implemented yet")
        return sys.exit(1)

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
