# 导入Flask类库
from flask import Flask, request, render_template
from search_kg import search
import os
# 创建应用实例
app = Flask(__name__)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"


@app.route("/")
def get_index():
    return render_template("index.html")



# 视图函数（路由）
@app.route('/kg_math/search')
def query():
    args = request.args
    query = args.get('q')
    return search(query)


# 启动实施（只在当前模块运行）
if __name__ == '__main__':
	app.run(debug=True,port=5000)
