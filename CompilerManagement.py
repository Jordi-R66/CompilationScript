from json import load, dump

KNOWN_COMPILERS: list[str] = [
	"gcc", "g++"
]

KNOWN_SYSTEMS: list[str] = [
	"linux", "win"
]

KNOWN_ARCHS: list[str] = [
	"i686", "AMD64", "ARM32", "ARM64"
]

COMPILERS: dict[str: str] = {}
UNAVAILABLE_COMPILER: str = "UNAVAILABLE"

def GenerateCompilersFile(reset_compilers_global: bool=False) -> None:
	compilers: dict[str: str] = {}

	for compiler in KNOWN_COMPILERS:
		for systems in KNOWN_SYSTEMS:
			for archs in KNOWN_ARCHS:
				compilers[f"{compiler} {systems} {archs}"] = UNAVAILABLE_COMPILER

	fp = open("compilers.json", "w", encoding="utf8")
	dump(compilers, fp, ensure_ascii=False, indent=4)
	fp.close()

	if reset_compilers_global:
		COMPILERS = dict(compilers)

def LoadCompilersFile() -> dict[str: str]:
	global COMPILERS

	fp = open("compilers.json", "r", encoding="utf8")

	data: dict[str: str] = load(fp)
	COMPILERS = dict(data)

	return dict(data)

def PickPreciseCompiler(compiler_name: str, target_system: str, target_arch: str, COMPILERS_DICT: dict = COMPILERS) -> str:
	if not (compiler_name.lower() in KNOWN_COMPILERS):
		raise Exception(f"Unknown compiler \"{compiler_name}\"")

	if not (target_system.lower() in KNOWN_SYSTEMS):
		raise Exception(f"Unknown system \"{target_system}\"")

	if not (target_arch in KNOWN_ARCHS):
		raise Exception(f"Unknown architecture \"{target_arch}\"")

	compiler_id: str = f"{compiler_name} {target_system} {target_arch}"

	compiler: str = COMPILERS_DICT.get(compiler_id)

	if (compiler != UNAVAILABLE_COMPILER):
		return compiler
	else:
		raise Exception(f"Can't find a compiler matching that string \"{compiler_id}\"")

if __name__ == "__main__":
	pass
