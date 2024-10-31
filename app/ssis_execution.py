import subprocess
import os

def run_ssis_package(package_name):
    package_path = os.path.join(os.path.dirname(__file__), 'ssis_packages', package_name)
    dtexec_command = f'dtexec /f "{package_path}"'
    
    try:
        result = subprocess.run(dtexec_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("SSIS package ran successfully.")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Failed to run SSIS package: {package_name}")
        print(e.stderr.decode())

if __name__ == "__main__":
    # Example: Running both SSIS packages
    run_ssis_package('OLTP_to_OLAP_DimensionTables.dtsx')
    run_ssis_package('OLTP_to_OLAP_FactRev.dtsx')
