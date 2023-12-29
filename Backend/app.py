# 导入Flask类库
from flask import Flask
from search_kg import search
# 创建应用实例
app = Flask(__name__)

# 视图函数（路由）
@app.route('/kg_math/search/<query>')
def query(query):
	return search(query)
# 启动实施（只在当前模块运行）
if __name__ == '__main__':
	app.run(debug=True,port=5000)
