import os
import sys
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description="BlenderHQ Addon Base batch run unit tests")
    parser.add_argument("-d", "--dir_blender", action='append',
                        help="The path to the directory containing the Blender executable file. It is recommended that "
                        "you use all paths to the Blender versions available for testing at once.")

    parser.add_argument("-b", "--background", action='store_true',
                        help="If you enter this argument, the test will be performed in the background, otherwise a "
                        "new instance of Blender will be opened in the window sequentially.")

    parser.add_argument("-i", "--wait_for_input", action='store_true',
                        help="Wait for the introduction before running the new Blender instance.")

    parser.add_argument("-s", "--use_default_win32_pathes", action='store_true',
                        help="Use the standard Windows installation paths.")

    args = parser.parse_args()

    blender_dirs = args.dir_blender
    if blender_dirs is None:
        blender_dirs = []

    if args.use_default_win32_pathes:
        base_win32_blender_path = 'C:/Program Files/Blender Foundation/Blender'

        # Special case for Blender 2.80
        blender_2_80_path = base_win32_blender_path
        if os.path.isdir(blender_2_80_path) and blender_2_80_path not in blender_dirs:
            blender_dirs.append(blender_2_80_path)
        del blender_2_80_path

        # Later versions.
        for version_major in range(2, 5):  # NOTE: range max may be less.
            for version_minor in range(0, 99):
                version_suffix = f" {version_major}.{version_minor}"
                bdir = base_win32_blender_path + version_suffix
                if os.path.isdir(bdir) and bdir not in blender_dirs:
                    blender_dirs.append(bdir)

    run_in_background = args.background
    wait_for_input = args.wait_for_input

    if not blender_dirs:
        parser.print_help()
        return

    for i, bdir in enumerate(blender_dirs):
        bfp = os.path.join(os.path.realpath(bdir), "blender")
        if sys.platform == 'win32':
            bfp += ".exe"
        elif sys.platform == 'linux':
            pass
        elif sys.platform == 'darwin':
            pass

        if not os.path.isfile(bfp):
            print(f"Blender executable not found by path \"{bfp}\", test skipped.")
            continue
        else:
            cli_args = [
                bfp,
                "--factory-startup",
                "--addons", "bhq_addon_base",
                "--python-expr", "import bpy; bpy.ops.bhqabt.unit_tests_all('EXEC_DEFAULT')",
                "--enable-autoexec",
            ]

            if run_in_background:
                cli_args.append("--background")

            print('_' * 119)

            proc = subprocess.Popen(cli_args)

            proc.wait()

            if wait_for_input and i < len(blender_dirs) - 1:
                input('\033[92m' + "Waiting for input to start the test in the next version..." + '\033[0m')


if __name__ == "__main__":
    main()
