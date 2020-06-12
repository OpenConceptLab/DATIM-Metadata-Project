"""
Use to import starter content into OCL to initialize the PEPFAR DATIM environment.
Before running, edit import_filenames variable with the list of files you wish to import.

Files:
* datim_init_all.json - Do this first - imports PEPFAR Org and sources for MER,SIMS,Mechanisms,Tiered-Site-Support
* datim_init_only_moh.json - imports DATIM-MOH sources, collections, and null_disag concepts for both FY18 and FY19
* dhis2datasets.json - imports OCL collections that stay in sync with a DHIS2 Dataset must be pre-defined in OCL.
  Required for MER, SIMS, and Tiered Site Support (not needed for DATIM-MOH or Mechanisms). Includes collections and
  their initial empty repo versions.
* tiered_support.json - Tiered site support content is static so it does not have a sync script. The content can
  simply be imported using this JSON file. Includes Concepts and Mappings for Tiered Site Support. Note that no
  repo versions and no collection references are created for Tiered Site Support
"""
import ocldev.oclfleximporter
import ocldev.oclresourcelist
import settings


# Edit this list to import the files that you need
import_filenames_all = [
    'init/pepfar_org.json',
    'init/datim_moh_fy18.json',
    'init/datim_moh_fy19.json',
]
import_filenames = import_filenames_all

# OCL Settings - JetStream Staging user=datim-admin
ocl_api_url_root = settings.ocl_api_url_qa
ocl_api_token = settings.api_token_qa_root

# Build a combined resource list
resource_list = ocldev.oclresourcelist.OclJsonResourceList()
for import_filename in import_filenames:
    resource_list = resource_list + ocldev.oclresourcelist.OclJsonResourceList.load_from_file(filename=import_filename)

# Process as bulk import
if resource_list:
    bulk_import_response = ocldev.oclfleximporter.OclBulkImporter.post(
        input_list=resource_list, api_token=ocl_api_token, api_url_root=ocl_api_url_root)
    task_id = bulk_import_response.json()['task']
    print 'BULK IMPORT TASK ID: %s' % task_id
    import_results = ocldev.oclfleximporter.OclBulkImporter.get_bulk_import_results(
        task_id=task_id, api_url_root=ocl_api_url_root, api_token=ocl_api_token,
        delay_seconds=5, max_wait_seconds=800)
    if import_results:
        print import_results.display_report()