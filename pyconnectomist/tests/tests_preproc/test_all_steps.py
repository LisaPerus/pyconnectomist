##########################################################################
# NSAp - Copyright (C) CEA, 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Mocking Popen directly - need to construct a Mock to return, and adjust its
communicate() return_value.
The benefit of this approach is in not needing to do the strip/split on your
fake return string.
"""

# System import
import unittest
import sys
import os
import copy
import numpy
# COMPATIBILITY: since python 3.3 mock is included in unittest module
python_version = sys.version_info
if python_version[:2] <= (3, 3):
    import mock
    from mock import patch
else:
    import unittest.mock as mock
    from unittest.mock import patch

# pyConnectomist module
from pyconnectomist.preproc.all_steps import complete_preprocessing
from pyconnectomist.preproc.all_steps import steps


class ConnectomistPreproc(unittest.TestCase):
    """ Test the Connectomist runs all preprocessing tabs function:
    'pyconnectomist.preproc.all_steps.complete_preprocessing'
    """
    def setUp(self):
        """ Define function parameters.
        """
        self.kwargs = {
            "dwi": "/my/path/mock_dwi.nii.gz",
            "bval": "/my/path/mock_dwi.bval",
            "bvec": "/my/path/mock_dwi.bvec",
            "outdir": "/my/path/mock_outdir",
            "subject_id": "Lola",
            "delta_TE": 5,
            "partial_fourier_factor": 1,
            "parallel_acceleration_factor": 2,
            "b0_magnitude": "/my/path/mock_b0_magnitude",
            "b0_phase": "/my/path/mock_b0_phase",
            "path_connectomist": "/my/path/mock_connectomist",
            "invertX": True,
            "invertY": False,
            "invertZ": False,
            "negative_sign": False,
            "echo_spacing": 1,
            "EPI_factor": None,
            "b0_field": 3.0,
            "water_fat_shift": 4.68,
            "delete_steps": True,
            "morphologist_dir": "/my/path/mock_morphologist",
            "manufacturer": "Siemens"
        }

    @mock.patch("pyconnectomist.preproc.all_steps."
                "data_import_and_qspace_sampling")
    @mock.patch("pyconnectomist.preproc.all_steps.rough_mask_extraction")
    @mock.patch("pyconnectomist.preproc.all_steps.outlying_slice_detection")
    @mock.patch("pyconnectomist.preproc.all_steps.susceptibility_correction")
    @mock.patch("pyconnectomist.preproc.all_steps.eddy_and_motion_correction")
    @mock.patch("pyconnectomist.preproc.all_steps."
                "export_eddy_motion_results_to_nifti")
    @mock.patch("pyconnectomist.preproc.all_steps.dwi_to_anatomy")
    @mock.patch("shutil.rmtree")
    @mock.patch("shutil.copy")
    @mock.patch("os.mkdir")
    def test_normal_execution(self, mock_mkdir, mock_copy, mock_rmtree,
                              mock_registration, mock_expeddy, mock_eddy,
                              mock_susceptibility, mock_outliers, mock_mask,
                              mock_qspace):
        """ Test the normal behaviour of the function.
        """
        # Set the mocked functions returned values
        mock_expeddy.return_value = ("mock_dwi", "mock_bval", "mock_bvec")

        # Test execution
        output_files = complete_preprocessing(**self.kwargs)
        mock_copy.assert_called_once_with(
            os.path.join(self.kwargs["outdir"], steps[2], "outliers.py"),
            self.kwargs["outdir"])
        expected_rmtree_calls = []
        for dirname in steps[:-1]:
            expected_rmtree_calls.append(
                mock.call(os.path.join(self.kwargs["outdir"], dirname)))
        self.assertTrue(expected_rmtree_calls == mock_rmtree.call_args_list)
        self.assertTrue(output_files == mock_expeddy.return_value)


if __name__ == "__main__":
    unittest.main()
