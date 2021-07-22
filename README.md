# Licsber 工具箱

## 代码说明

个人娱乐, 供参考.

## Shell命令介绍

licsber: Hello world.  
count-dir: 统计目录下的文件与目录数.  
flatten-dir: 递归展开当前目录下所有子文件夹到当前目录.  
empty-dir: 递归删除当前目录下所有空文件夹.    
memobird: 发送咕咕机消息.  
archive: 生成当前目录下的所有文件的SHA1和CRC32校验码.

## 版本说明

2.6.0 增加archive命令.  
2.4.0 部分重构项目目录 修复S3Saver创建bucket.  
2.3.2 mongo+minio分别存储元数据与文件本身.  
2.2.1 mongo获取最新数据(sort+limit)函数.  
2.1.2 优化验证码模型为3通道直接输入 完全端到端.  
2.1.0 新增PaddlePaddle验证码识别模型.  
2.0.0 增加cv.imshow 自动转化bgr为rgb.  
1.8.0 更改get_mongo的连接行为.  
1.7.3 更改empty-dir也会删除.DS_Store.  
1.7.1 增加删除空文件夹命令empty-dir.   
1.6.0 增加腾讯云API网关hmac签名算法.  
1.5.0 增加离线S3存储签名功能.  
1.4.3 增加random_get方法project参数.  
1.4.2 mongo改为默认连接时connect=False.  
1.4.0 增加mongo的random_get方法.  
1.3.0 迁移spider函数, 增加mul_get方法.  
1.2.0 增加ml处理xyxy和xywh相互转换.  
1.1.0 增加log_message函数.   
1.0.1 增加注释.  
1.0.0 移除pycrypto 替换为pycryptodome.  
0.2.0 增加咕咕机提醒功能.  
0.1.0 增加wisedu的登录api.  
0.0.12 增加shell命令 flatten-dir.  
0.0.7 增加shell命令 count-dir.  
0.0.6 增加了邮件提醒功能.  
0.0.4 增加获取mongo数据库功能.

## 更新说明

x.y.z  
x: 不兼容的大更新 如依赖库发生的改变  
y: 兼容的功能更新  
z: bug fix

中间被略过的版本一般是bug fix, 切记不要使用.  
