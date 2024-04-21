import os
import sys


def basic_file_structure() -> str:
    """create basic file structure"""
    current_path = os.getcwd()

    # create project directories
    try:
        # dont use exist=True, it will not raise an error if the directory already exists # noqa
        os.makedirs(current_path + f"/{sys.argv[1]}")

    except FileExistsError:
        print("Project already exists")
        return sys.exit()

    except IndexError:
        print("Please provide an argument like: 'project_name'")
        return sys.exit()

    except Exception as e:
        print(e)
        return sys.exit()

    # create subdirectories
    os.makedirs(current_path + f"/{sys.argv[1]}/requirements")

    # create files dev_requirements.txt, requirements.txt
    open(
        current_path + f"/{sys.argv[1]}/requirements/dev_requirements.txt", "w"
    ).close()
    open(current_path + f"/{sys.argv[1]}/requirements/requirements.txt", "w").close()  # noqa

    open(current_path + f"/{sys.argv[1]}/.gitignore", "w").close()

    open(current_path + f"/{sys.argv[1]}/README.md", "w").close()

    open(current_path + f"/{sys.argv[1]}/LICENSE", "w").close()

    open(current_path + f"/{sys.argv[1]}/setup.py", "w").close()

    open(current_path + f"/{sys.argv[1]}/main.py", "w").close()

    # return the project directory
    return current_path + f"/{sys.argv[1]}"


def create_virtual_environment():
    """create virtual environment"""
    # ask user if they want to create a virtual environment
    print("Do you want to create a virtual environment? (y/n)")
    c_venv = input()

    # if yes, create a virtual environment
    if c_venv == "y" or "yes":
        os.system(f"python3 -m venv {sys.argv[1]}/venv")
        print("Virtual environment created with the name: venv")
    else:
        print("Virtual environment will not be created")


def main():
    print("Project generator started")


if __name__ == "__main__":
    main()
    # zsh got to the directory
    basic_file_structure()
    create_virtual_environment()
