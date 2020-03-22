#!/bin/bash

path_to_dir00="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/"




path_to_dir01="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/early/"

path_to_dir02="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/later/"



path_to_dir1="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/early/removeevoked/"

path_to_dir2="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/later/removeevoked/"


path_to_dir3="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/early/resampled/"

path_to_dir4="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/later/resampled/"


path_to_dir5="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/early/none/"

path_to_dir6="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/later/none/"



path_to_dir7="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/early/non_symm/"

path_to_dir8="/pl/active/ccnlab/users/zolfaghar/finalCodes_version5.2/decoding/decoding_designedFilter/datasets/later/non_symm/"





if [ -d $path_to_dir00 ]
then
    echo "Directory $path_to_dir00 exists."
else
    echo "Directory $path_to_dir00 does not exists. Now created"
    mkdir "$path_to_dir00"
fi

    


if [ -d $path_to_dir01 ]
then
    echo "Directory $path_to_dir01 exists."
else
    echo "Directory $path_to_dir01 does not exists. Now created"
    mkdir "$path_to_dir01"
fi

if [ -d $path_to_dir02 ]
then
    echo "Directory $path_to_dir02 exists."
else
    echo "Directory $path_to_dir02 does not exists. Now created"
    mkdir "$path_to_dir02"
fi




if [ -d $path_to_dir1 ]
then
    echo "Directory $path_to_dir1 exists."
else
    echo "Directory $path_to_dir1 does not exists. Now created"
    mkdir "$path_to_dir1"
fi

if [ -d $path_to_dir2 ]
then
    echo "Directory $path_to_dir2 exists."
else
    echo "Directory $path_to_dir2 does not exists. Now created"
    mkdir "$path_to_dir2"
fi


if [ -d $path_to_dir3 ]
then
    echo "Directory $path_to_dir3 exists."
else
    echo "Directory $path_to_dir3 does not exists. Now created"
    mkdir "$path_to_dir3"
fi


if [ -d $path_to_dir4 ]
then
    echo "Directory $path_to_dir4 exists."
else
    echo "Directory $path_to_dir4 does not exists. Now created"
    mkdir "$path_to_dir4"
fi


if [ -d $path_to_dir5 ]
then
    echo "Directory $path_to_dir5 exists."
else
    echo "Directory $path_to_dir5 does not exists. Now created"
    mkdir "$path_to_dir5"
fi


if [ -d $path_to_dir6 ]
then
    echo "Directory $path_to_dir6 exists."
else
    echo "Directory $path_to_dir6 does not exists. Now created"
    mkdir "$path_to_dir6"
fi


if [ -d $path_to_dir7 ]
then
    echo "Directory $path_to_dir7 exists."
else
    echo "Directory $path_to_dir7 does not exists. Now created"
    mkdir "$path_to_dir7"
fi


if [ -d $path_to_dir8 ]
then
    echo "Directory $path_to_dir8 exists."
else
    echo "Directory $path_to_dir8 does not exists. Now created"
    mkdir "$path_to_dir8"
fi
wait
