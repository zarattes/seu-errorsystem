1、所需环境
    -anaconda版本为2020.11
    -python版本为3.6.8
    -创建虚拟环境：conda create -n nlp python=3.6 
    -安装包:pip install -r D:\学习资料\model\requirements.txt（txt路径为绝对路径,自行更改）
    -根据自己的文件位置修改config中的bert_config_path和similar_config_path
2、项目结构：
    --checkpoint
        模型文件
    --data
        /columns 列名
        /labels 运维类型
        /train.csv 处理后的训练数据
        /test.csv 处理后的测试数据
        /问题汇总(2)(1).xlsx 原始数据
    --bert_model.py bert分类模型
    --bert_server.py bert分类服务
    --config.py 配置文件
    --flask_server.py 项目总入口(web服务)
    --process_data.py 数据预处理
    --similar.py 句子相似度计算(web服务)
    --train.py 训练bert模型
    --requirements.txt 项目相关库
3、anaconda中启动bert_server,similar （根据路径自行调整）
   激活环境
   进入项目目录
   python bert_server.py 
   python similar.py 
4、启动server（用这个启动服务）
   python flask_server.py   （根据路径自行调整）
5、服务调用：
    接口：http://127.0.0.1:6003/api/classifier
    参数：{"text":"需要解答的问题"}