##!/usr/bin/env python3

from os import path, mkdir, system
from sys import platform
from json import loads, dump

from pprint import pprint

from CompilerManagement import *

EXTS: dict[str: str] = {
	"default": "",
	"win": ".exe",
	"linux": ".elf",
}

if platform not in ("win32", "linux"):
	platform = "default"

EXEC_EXT: str = EXTS[platform]

def compile(compiler: str, compiler_args: list[str], output: str, sources: list[str], use_math: bool=True):
	sources_string: str = " ".join(sources)
	lm: str = " -lm" if ((platform == "linux") & (use_math)) else ""
	compile_command: str = f"{compiler} {compiler_args} {sources_string} -o {output}{EXEC_EXT}{lm}"

	print(f"Compilation command : {compile_command}")

	system(compile_command)

def generateCompileConf(name: str):
	if not name.endswith(".json"):
		name = f"{name}.json"

	fp = open(name, "w", encoding="utf8")

	COMPILE_CONFIG: dict[str] = {
		"Compiler": "",
		"TargetSystem": "",
		"TargetArch": "",
		"Parameters": [],
		"OutputPath": "",
		"OutputName": "",
		"Sources": [],
		"UseMath": False
	}

	dump(COMPILE_CONFIG, fp, indent=4, ensure_ascii=False)
	fp.close()

def LetsCompile(ConfName: str="compile_conf.json"):
	if path.exists(ConfName):
		valid_steps: int = 0

		fp = open(ConfName, "r", encoding="utf8")
		raw_content: str = fp.read()
		fp.close()

		valid_steps += 1

		COMPILE_CONFIG: dict = loads(raw_content)

		if not (isinstance(COMPILE_CONFIG, dict) & (len(COMPILE_CONFIG) == 6)):
			raise Exception(f"Impossible d'extraire les données du json\n\n{raw_content}")
		
		valid_steps += 1

		COMPILER: str = COMPILE_CONFIG.get("Compiler")
		PARAMS_LIST: list[str] = COMPILE_CONFIG.get("Parameters")
		OUTPUT_PATH: str = COMPILE_CONFIG.get("OutputPath")
		OUTPUT_NAME: str = COMPILE_CONFIG.get("OutputName")
		USE_MATH: bool = COMPILE_CONFIG.get("UseMath")

		SOURCE_FILES: list[str] = COMPILE_CONFIG.get("Sources")

		if (None in (COMPILER, PARAMS_LIST, OUTPUT_PATH, OUTPUT_NAME, SOURCE_FILES)):
			raise Exception("Erreur préliminaire : Une valeur ou plus n'a pas pu être récupérée dans le fichier config")

		valid_steps += 1

		if (isinstance(PARAMS_LIST, list)) & (len(PARAMS_LIST) > 0) & (PARAMS_LIST is not None):
			PARAMS: str = " ".join(PARAMS_LIST)
		else:
			raise Exception("Erreur préliminaire : Un problème est survenu lors de la lecture des paramètres de compilation")

		valid_steps += 1

		currentPath: str = ""
		for Folder in OUTPUT_PATH.split("/"):
			exists: bool = path.exists(f"{currentPath}/{Folder}")

			if not (exists):
				mkdir(f"{currentPath}/{Folder}")
			
			currentPath = f"{currentPath}/{Folder}"

		valid_steps += 1

		if (len(SOURCE_FILES) == 0):
			raise Exception("Erreur préliminaire : Aucun fichier source n'a été spécifié")

		valid_steps += 1

		for File in SOURCE_FILES:
			exists: bool = path.exists(File)

			valid_steps += 1

			if not exists:
				raise Exception(f"Erreur préliminaire : \"{File}\" est introuvable")

		valid_steps += 1

		OUTPUT = f"{OUTPUT_PATH}{OUTPUT_NAME}"

		if valid_steps >= 7:
			compile(COMPILER, PARAMS, OUTPUT, SOURCE_FILES, USE_MATH)
	else:
		generateCompileConf(ConfName)

if __name__ == "__main__":
	#LetsCompile()

	GenerateCompilersFile()
