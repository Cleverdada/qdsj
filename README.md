# crm数据同步文档
###流程：
- 同步脚本每次push数据前会向crm请求当前表的最大id(api/tb/max_id)，以便于增量同步,获取到max_id后，客户端会在本地数据库中找到大于max_id的所有数据向crm进行推送

###接口约定：
1. api/tb/max_id:
 
	`获取table对应的最大id`
	
	* 请求方式: Get
	* 请求参数约定：

		|  参数 | 参数描述|类型 |是否必填|
		|:------- |:-----------|:-----------|:-----------|
		| ds_name | 数据库名称 |String|必填|
		| tb_name | 数据表名称 |String|必填|
	
	* 返回参数示例

		``` json
		{
		"status": 0,  // 0 表示成功
    "errstr": "",  // status 非0 时，需要给出错误描述
    "result": {
        "max_id": 1000   //工作表ID
    }
    "request_id": "xxxxxx"   //请求唯一标识id，方便排查错误    
    }
		```

2. api/tb/push:

	`将客户端数据推送到crm系统`
	* 请求方式： Post
	* 请求参数约定：

		|  参数 | 参数描述|类型 |是否必填|
		|:------- |:-----------|:-----------|:-----------|
		| ds_name | 数据库名称 |String|必填|
		| tb_name | 数据表名称 |String|必填|
		| fields | 字段名列表|Array|必填|
		| data | 数据集合|二维Array|必填|
		| extra_field | 辅助字段，用于标识表的来源|String|非必填|
		
	
	* 返回参数示例

		``` json
		{
		"status": 0,  // 0 表示成功
    "errstr": "",  // status 非0 时，需要给出错误描述
    "result": "success"
    "request_id": "xxxxxx"   //请求唯一标识id，方便排查错误    
    }
		```