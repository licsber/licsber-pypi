# Licsber 工具箱

## 代码说明

个人娱乐, 供参考.

## Shell命令介绍

licsber: Hello world.  
memobird: 发送咕咕机消息.  
count-dir: 统计目录下的文件与目录数.  
flatten-dir: 递归展开当前目录下所有子文件夹到当前目录.  
empty-dir: 递归删除当前目录下所有空文件夹.    
archive: 生成当前目录下的所有文件的SHA1和MD5校验码.   
rename: 将单个目录内所有文件重命名为SHA1值.  
save-115: 将目录下所有文件保存为115Link形式.  
save-115-dir: 递归将整个目录目录保存为115Link形式.  
conv: 将115Link转化为阿里云盘Link.

## 主要包介绍

cv: 数据集拍照助手|notebook环境imshow  
datasets: 个人制作发布的数据集(仅在群里公开过)  
mail: 含一个美化过的提醒模板用于bot任务  
ml: MachineLearning常用的封装  
mongo: PyMongo的封装|与s3配合可以实现一个元数据与内容分离的FS  
s3: MinIO库的封装|包含离线制作OSS签名|随机取OSS内容  
shell: licsber库提供的shell命令|查看代码后谨慎使用  
spider: 爬虫封装|获取自定义session|多线程下载  
utils: 标准库封装 不会出现任何第三方库  
wisedu: 金智教务验证码识别|模拟登录|腾讯云函数hmac认证  
github: 用于Github Actions的封装

## 版本说明

5.1.5 增加基础cifar10分类示例.  
5.0.0 依赖torch和torchvision.  
4.5.0 增加ThreadPoolExecutor与tqdm的封装.  
4.4.4 增加batch_update函数.  
4.4.1 增加爬虫使用的check_force函数.  
4.4.0 增加get_s3函数获取S3对象存储.  
4.3.0 rename命令增加文件size防sha-1碰撞.  
4.2.2 增加save-115-dir命令的缓存功能.  
4.1.3 修复wisedu模块找不到模型问题.  
4.1.2 重构umeta 现在额外兼容了百度网盘梦姬格式.  
4.0.1 重构 改进部分依赖为可选依赖 兼容嵌入式设备.  
3.4.2 save-115-dir时忽略QNAP缓存文件.  
3.3.1 兼容gawwo/fake115-go的文件夹格式.  
3.2.2 优化utils.umeta的内存占用.  
3.1.0 增加115链接格式转换阿里云盘.  
3.0.1 增加tqdm依赖.  
2.8.0 增加递归获取115链接.  
2.7.4 增加rename命令.  
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

## 环境变量

```bash
export L_MONGO_HOST='mongodb://{mongo服务器地址}'
export MONGO_PASSWD_B64='{mongo服务器密码}'
export L_S3_ENDPOINT='{s3服务器地址 不带schema}'
export L_S3_ACCESS='{s3服务器ak}'
export L_S3_SECRET='{s3服务器sk}'
export DATASETS_ROOT='{数据集文件夹根目录}'
export CHECKPOINT_ROOT='{训练中间文件目录}'
```
