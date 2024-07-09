from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="votre-api-flask",
    version="0.1.0",
    author="Muller Thomas",
    author_email="votre.email@exemple.com",
    description="Une API Flask sécurisée pour la gestion des utilisateurs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-username/votre-repo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Flask>=2.0.0",
        "Flask-RESTful>=0.3.9",
        "Flask-Limiter>=1.4",
        "Flask-JWT-Extended>=4.3.0",
        "Flask-CORS>=3.0.10",
        "bcrypt>=3.2.0",
        "python-dotenv>=0.19.0",
        "qrcode>=7.3",
        "google-auth-oauthlib>=0.4.6",
        "google-auth-httplib2>=0.1.0",
        "google-api-python-client>=2.26.1",
    ],
    entry_points={
        "console_scripts": [
            "run-api=MSPR_CAFE_FLASK_BASE.main:main",
        ],
    },
)