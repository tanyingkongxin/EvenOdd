#!/bin/bash

cd ..
rm -rf build/disk_*
rm -rf build/test_data
rm build/error_log.txt

./compile.sh
mv time_check build/
mv evenodd build/

cd build
mkdir test_data

if [ $# != 2 ]; then
    echo "usage: bash correct.sh <file_size> <prime>"
    exit 1
fi

file_size=`expr $1 \* 1073741824`
index_1=0
index_2=0
prime=$2

src="/mnt/vdb/wxr/data_${1}GB"
#src="../wxr_script/data/data_${1}GB"

#测试write模块时间
./time_check write $src $prime

## test no filed failed
echo ====================================
./time_check read ${src} ./test_data/data_read_0

result=`diff ${src} ./test_data/data_read_0`
if [ -n "$result" ]
then
    echo "test no file failed" >> error_log.txt
    echo "此时素数取值为:$prime  文件大小为: ${file_size}B" >> error_log.txt
    echo "$result" >> error_log.txt
    echo "===============================================" >> error_log.txt
fi
rm -rf ./test_data/data_read_0
echo ====================================

## test two files failed
### case 1:

let "index_1=prime"
let "index_2=prime+1"
mv disk_$index_1 _disk_$index_1
mv disk_$index_2 _disk_$index_2
./time_check read $src ./test_data/data_read_21
result=`diff ${src} ./test_data/data_read_21`
if [ -n "$result" ]
then
    echo "case 1" >> error_log.txt
    echo "删除掉disk_${index_1}和disk_${index_2} read失败" >> error_log.txt
    echo "此时素数取值为:$prime  文件大小为: ${file_size}B" >> error_log.txt
    echo "$result" >> error_log.txt
    echo "===============================================" >> error_log.txt

fi
mv _disk_$index_1 disk_$index_1
mv _disk_$index_2 disk_$index_2
rm -rf ./test_data/data_read_21
echo ====================================
# ### case 2:
let "index_1=prime-2"
let "index_2=prime"
mv disk_$index_1 _disk_$index_1
mv disk_$index_2 _disk_$index_2
./time_check read $src ./test_data/data_read_22
result=`diff ${src} ./test_data/data_read_22`
if [ -n "$result" ]
then
    echo "case 2" >> error_log.txt
    echo "删除掉disk_${index_1}和disk_${index_2} read失败" >> error_log.txt
    echo "此时素数取值为:$prime  文件大小为: ${file_size}B" >> error_log.txt
    echo "$result" >> error_log.txt
    echo "==============================================" >> error_log.txt

fi
mv _disk_$index_1 disk_$index_1
mv _disk_$index_2 disk_$index_2
rm -rf ./test_data/data_read_22
echo ====================================
# ### case 3:
let "index_1=prime-1"
let "index_2=prime+1"
mv disk_$index_1 _disk_$index_1
mv disk_$index_2 _disk_$index_2
./time_check read $src ./test_data/data_read_23

result=`diff ${src} ./test_data/data_read_23`
if [ -n "$result" ]
then
    echo "case 3" >> error_log.txt
    echo "删除掉disk_${index_1}和disk_${index_2} read失败" >> error_log.txt
    echo "此时素数取值为:$prime  文件大小为: ${file_size}B" >> error_log.txt
    echo "$result" >> error_log.txt
    echo "===============================================" >> error_log.txt

fi
mv _disk_$index_1 disk_$index_1
mv _disk_$index_2 disk_$index_2
rm -rf ./test_data/data_read_23
echo ====================================

# ### case 4:
let "index_1=prime-2"
let "index_2=prime-1"
mv disk_$index_1 _disk_$index_1
mv disk_$index_2 _disk_$index_2
./time_check read $src ./test_data/data_read_24

result=`diff ${src} ./test_data/data_read_24`
if [ -n "$result" ]
then
    echo "case 4" >> error_log.txt
    echo "删除掉disk_${index_1}和disk_${index_2} read失败" >> error_log.txt
    echo "此时素数取值为:$prime  文件大小为: ${file_size}B" >> error_log.txt
    echo "$result" >> error_log.txt
    echo "===============================================" >> error_log.txt

fi
mv _disk_$index_1 disk_$index_1
mv _disk_$index_2 disk_$index_2
rm -rf ./test_data/data_read_24
echo ====================================

# ### case 5:
let "index_1=prime-2"
let "index_2=prime-3"
mv disk_$index_1 _disk_$index_1
mv disk_$index_2 _disk_$index_2
./time_check read $src ./test_data/data_read_25

result=`diff ${src} ./test_data/data_read_25`
if [ -n "$result" ]
then
    echo "case 5" >> error_log.txt
    echo "删除掉disk_${index_1}和disk_${index_2} read失败" >> error_log.txt
    echo "此时素数取值为:$prime  文件大小为: ${file_size}B" >> error_log.txt
    echo "$result" >> error_log.txt
    echo "===============================================" >> error_log.txt


fi
mv _disk_$index_1 disk_$index_1
mv _disk_$index_2 disk_$index_2
rm -rf ./test_data/data_read_25
echo ====================================

# rm -rf disk*
# rm -rf test*
