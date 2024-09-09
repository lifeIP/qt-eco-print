./CMD/xinput/get_difference.sh

inputs=($(cat ./CMD/xinput/files/result))

for i in "${inputs[@]}"; do
  xinput --disable $i
done