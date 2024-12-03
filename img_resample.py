import os
import SimpleITK as sitk

def main():
    # resample test images to atlas image (same size --> segmentation overlay) and save them
    # can be used for segmentation overlay on T1, T2 image

    script_dir = os.path.dirname(os.path.realpath(__file__))
    atlas_dir = os.path.join(script_dir, 'data/atlas')
    test_dir = os.path.join(script_dir, 'data/test')

    atlasT1 = sitk.ReadImage(os.path.join(atlas_dir, 'mni_icbm152_t1_tal_nlin_sym_09a_mask.nii.gz'))

    for subdir, dirs, files in os.walk(test_dir):
        for dir in dirs:
            transform_path = os.path.join(test_dir, dir, 'affine.txt')
            imageT1_path = os.path.join(test_dir, dir, 'T1native.nii.gz')
            imageT2_path = os.path.join(test_dir, dir, 'T2native.nii.gz')
            imageLabels_path = os.path.join(test_dir, dir, 'labels_native.nii.gz')

            # load data
            transform = sitk.ReadTransform(transform_path)
            imageT1 = sitk.ReadImage(imageT1_path)
            imageT2 = sitk.ReadImage(imageT2_path)
            imageLabels = sitk.ReadImage(imageLabels_path)

            # resample data
            imageT1_resampled = sitk.Resample(image1=imageT1, referenceImage=atlasT1, transform=transform,
                                              interpolator=sitk.sitkLinear, defaultPixelValue=0.0,
                                              outputPixelType=imageT1.GetPixelIDValue())
            imageT2_resampled = sitk.Resample(image1=imageT2, referenceImage=atlasT1, transform=transform,
                                             interpolator=sitk.sitkLinear, defaultPixelValue=0.0,
                                             outputPixelType=imageT2.GetPixelIDValue())
            imageLabels_resampled = sitk.Resample(image1=imageLabels, referenceImage=atlasT1, transform=transform,
                                              interpolator=sitk.sitkNearestNeighbor, defaultPixelValue=0.0,
                                              outputPixelType=imageT2.GetPixelIDValue())

            # copy image information after resample
            imageT1_resampled.CopyInformation(atlasT1)
            imageT2_resampled.CopyInformation(atlasT1)
            imageLabels_resampled.CopyInformation(atlasT1)

            # create resample folder
            save_dir = os.path.join(test_dir, dir, 'resampled')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # save resampled images
            sitk.WriteImage(imageT1_resampled, os.path.join(save_dir, 'T1native.nii.gz'), False)
            sitk.WriteImage(imageT2_resampled, os.path.join(save_dir, 'T2native.nii.gz'), False)
            sitk.WriteImage(imageLabels_resampled, os.path.join(save_dir, 'labels_native.nii.gz'), False)
        break # only go through first level of os.walk


if __name__ == '__main__':
    main()
