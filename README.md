# MCQ Generator

MCQ Generator is a Python project designed to automate the creation of Multiple Choice Questions (MCQs) from various sources. This tool aims to help educators, students, and content creators quickly generate, review, and export MCQs for quizzes, exams, and learning materials.

## Features
- Generate MCQs from text, documents, or other sources (feature placeholder)
- Customizable question and answer formats
- Export MCQs to different formats (CSV, JSON, etc.)
- Logging and utility functions for easy debugging and extension

## Project Structure
```
src/
  mcqgenerator/
	 __init__.py
	 mcqgenerator.py
	 utils.py
	 logger.py
experiment/
  mcqgenerator.ipynb
requirements.txt
setup.py
README.md
```

## Installation
1. Clone the repository:
	```sh
	git clone https://github.com/Vaibhav140705/MCQ-Generator.git
	cd MCQ-Generator
	```
2. (Optional) Create and activate a virtual environment:
	```sh
	python -m venv venv
	.\venv\Scripts\activate
	```
3. Install dependencies:
	```sh
	pip install -r requirements.txt
	```

## Usage
You can use the provided Jupyter notebook for experimentation:

```
jupyter notebook experiment/mcqgenerator.ipynb
```

Or import the package in your Python scripts:

```python
from src.mcqgenerator import mcqgenerator
# Example usage here
```

## Contributing
Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or improvements.

## License
This project is licensed under the MIT License.

## Contact
Created by Vaibhav140705. For questions or suggestions, please open an issue on GitHub.
