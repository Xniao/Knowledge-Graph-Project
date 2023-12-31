# 导入Flask类库
from flask import Flask, request, render_template
from search_kg import search,random_knowledge_point
import os
# 创建应用实例
app = Flask(__name__)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def get_index():
    return render_template("index.html")



# 视图函数（路由）
@app.route('/kg_math/search')
def query():
    args = request.args
    query = args.get('q')
    return search(query)


@app.route('/kg_math/random')
def query_random():
    return random_knowledge_point()


# 启动实施（只在当前模块运行）
if __name__ == '__main__':
	app.run(host="localhost", port=5000, threaded=True)
