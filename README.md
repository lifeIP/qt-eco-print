export QT_IM_MODULE=qtvirtualkeyboard
find / -name libstdc++.so.6 2>/dev/null
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6


# для работы преобразования docx to pdf
sudo apt-get install default-jre libreoffice-java-common