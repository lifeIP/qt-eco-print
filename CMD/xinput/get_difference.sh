comm -3 <(sort ./CMD/xinput/files/input1) <(sort ./CMD/xinput/files/input0) > ./CMD/xinput/files/result

inputs=($(cat ./CMD/xinput/files/result))