# 导入Flask类库
from flask import Flask
# 创建应用实例
app = Flask(__name__)
# 视图函数（路由）
@app.route('/index')
def index():
	return {'name':'123'}
# 启动实施（只在当前模块运行）
if __name__ == '__main__':
	app.run(debug=True,port=5000)
