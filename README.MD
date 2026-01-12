#### 项目部署
- 代码下载
``` shell
# 下载网页源代码
git clone https://github.com/likooooo/cat_planet.git
# 下载资源文件
cd cat_planet && git submodule update --init --recursive
```

- 初始化运行环境
``` shell
python3 -m venv env_cat_planet
source ./env_cat_planet/bin/activate
pip install --no-cache-dir -r requirements.txt
```

- 在本地启动服务
``` shell
streamlit run ./app.py --server.port=8501
# 访问网页 http://localhost:8501/
```
