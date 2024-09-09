./CMD/xinput/get_difference.sh

inputs=($(cat ./CMD/xinput/files/input1))

for i in "${inputs[@]}"; do xinput --enable $i; done