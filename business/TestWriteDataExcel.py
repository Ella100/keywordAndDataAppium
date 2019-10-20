from action.PageAction import *
from common.ParseExcel import ParseExcel
from config.VarConfig import *
import time
import traceback


# 创建解析Excel对象
excelObj = ParseExcel()

# 将Excel数据文件加载到内存
excelObj.loadWorkBook(dataFilePath)

# 用例或用例步骤执行结束后，向Excel中写执行结果信息
def writeTestResult(sheetObj,rowNo,colsNo,testResult,
                    errorInfo=None,picPath=None):
    # 测试通过结果信息为绿色，失败为红色
    colorDict = {"pass":"green","faild":"red"}

    # 因为“测试用例”工作表和“用例步骤sheet表”中都有测试执行时间和
    # 测试结果列，定义此字典对象为了区分具体应该写哪个工作表
    # 执行时间和结果列 是固定不变的
    colsDict = {
        "testCase":[testCase_runTime,testCase_testResult],
        "caseStep":[testStep_runTime,testStep_testResult],
        "dataSheet":[dataSource_runtime,dataSource_result]
    }

    try:


        # 在测试步骤sheet中，写入测试结果
        excelObj.writeCell(sheetObj,content=testResult,
                           rowNo=rowNo,colsNo=colsDict[colsNo][1],
                           style=colorDict[testResult])

        if testResult == "":
            # 清空时间单元格
            excelObj.writeCell(sheetObj,content="",
                               rowNo = rowNo,colsNo=colsDict[colsNo][0])
        else:
            # 在测试步骤中，写入测试时间
            excelObj.writeCellCurrentTime(sheetObj,
                                          rowNo=rowNo, colsNo=colsDict[colsNo][0],
                                          style=colorDict[testResult])

        if errorInfo and picPath:
            # 在测试步骤sheet中，写入异常信息
            excelObj.writeCell(sheetObj,content=errorInfo,
                               rowNo=rowNo,colsNo=testStep_errorInfo)
            # 在测试步骤sheet中，写入异常截图路径
            excelObj.writeCell(sheetObj,content=picPath,
                               rowNo=rowNo,colsNo=testStep_errorPic)

        else:
            if colsNo == "caseStep":
                # 在测试步骤sheet中，清空异常信息单元格
                excelObj.writeCell(sheetObj,content="",
                                   rowNo=rowNo,colsNo=testStep_errorInfo)

                # 在测试步骤sheet中，清空异常信息单元格
                excelObj.writeCell(sheetObj,content="",
                                   rowNo=rowNo,colsNo=testStep_errorPic)

    except  Exception as e:
        print("写excel错误", traceback.print_exc())


def dataDriverFun(dataSourceSheetObj,caseStepSheetName):
    try:
        # 通过sheet名称获取表单对象
        stepSheetObj = excelObj.getSheetByName(caseStepSheetName)
        # 获取数据源表中是否执行列对象
        dataIsExecuteColumn = excelObj.getColumn(dataSourceSheetObj,
                                                 dataSource_isExecute)
        #获取数据源表中“姓名”列对象
        usernameColumn = excelObj.getColumn(dataSourceSheetObj,dataSource_username)
        # 获取测试步骤表中存在数据区域的行数
        stepRowNums = excelObj.getRowsNumber(stepSheetObj)

        # 记录成功执行的数据条数
        successDatas = 0

        # 记录被设置为执行的数据条数
        requireDatas = 0

        for idx,data in enumerate(dataIsExecuteColumn[1:]):
            # 遍历数据源表，准备进行数据驱动测试
            # 因为第一行是标题行，所以第二行开始遍历
            if data.value == "y":
                print("开始登入[%s]" % usernameColumn[idx + 1].value)
                requireDatas += 1
                # 定义记录执行成功步骤数变量
                successfulSteps = 0
                for step in range(2,stepRowNums+1):
                    # 获取数据驱动测试步骤表中
                    # 第index行对象
                    stepRow = excelObj.getRow(stepSheetObj,step)
                    # 获取关键字作为调用的函数名
                    keyWord = stepRow[testStep_keyWords - 1].value
                    # 获取操作元素的定位方式作为调用函数的参数
                    locationType = stepRow[testStep_locationType - 1].value
                    # 获取操作元素的定位表达式作为调用函数的参数
                    locatorExpression = stepRow[testStep_locatorExpression - 1].value
                    # 获取操作值作为调用函数的参数
                    operateValue = stepRow[testStep_operateValue - 1].value

                    # 将操作为数字类型的数据转化字符串类型，方便字符串拼接
                    if isinstance(operateValue, int):
                        operateValue = str(operateValue)
                    # print(keyWord,locationType,locatorExpression,operateValue)
                    if operateValue and operateValue.isalpha():
                        # 如果operateValue变量不为空，说明有曹植
                        # 从数据源表中根据坐标获取对应单元格的数据
                        coordinate = operateValue + str(idx+2)
                        operateValue = excelObj.getCellOfValue(
                            dataSourceSheetObj,coordinate=coordinate
                        )


                    # 字符串的拼接
                    expressionStr = ""
                    # 构造需要执行的python语句
                    # 对应的PageAction.py文件中的页面动作函数调用的字符串表示
                    if keyWord and operateValue and \
                            locationType is None and locatorExpression is None:
                        expressionStr = keyWord.strip() + "('" + operateValue + "')"
                    elif keyWord and operateValue is None and \
                            locationType is None and locatorExpression is None:
                        expressionStr = keyWord.strip() + "()"
                    elif keyWord and locationType and operateValue \
                            and locatorExpression is None:
                        expressionStr = keyWord.strip() + \
                                        "('" + locationType.strip() + "','" + operateValue + "')"
                    elif keyWord and locationType and locatorExpression and \
                            operateValue:
                        expressionStr = keyWord.strip() + \
                                        "('" + locationType.strip() + "','" + \
                                        locatorExpression.replace("'", '""').strip() + \
                                        "','" + operateValue + "')"
                    elif keyWord and locationType and locatorExpression \
                            and operateValue is None:
                        expressionStr = keyWord.strip() + \
                                        "('" + locationType.strip() + "','" + \
                                        locatorExpression.replace("'", '""').strip() + "')"

                    try:
                        # 通过eval函数，将拼接的页面动作函数调用字符串表示
                        # 当成有效的Python表达式执行，从而执行测试步骤的sheet中
                        eval(expressionStr)

                        # 在测试执行时间写入列
                        excelObj.writeCellCurrentTime(stepSheetObj, rowNo=step,
                                                      colsNo=testStep_runTime)

                    except Exception as e:
                        # 获取异常屏幕图片
                        capturePic = getScreenShot(caseStepSheetName)
                        # 获取详细的异常堆栈信息
                        errorInfo = traceback.format_exc()
                        # 在测试步骤sheet中写入失败信息
                        writeTestResult(stepSheetObj, step, "caseStep", "faild", errorInfo, capturePic)

                        logging.info("用例[%s]步骤%d[%s]执行失败" % \
                                     (caseStepSheetName, step - 1, stepRow[testStep_testStepDescribe - 1].value))

                    else:
                        # 在测试步骤Sheet中写入成功信息
                        writeTestResult(stepSheetObj, step, "caseStep", "pass")
                        # 每成功一步，successfulSteps变量自增1
                        successfulSteps += 1
                        logging.info("用例[%s]步骤%d[%s]执行通过" % \
                                     (caseStepSheetName, step - 1, stepRow[testStep_testStepDescribe - 1].value))

                if stepRowNums == successfulSteps +1:
                    successDatas += 1
                    # 如果成功执行的步骤数等于步骤表中给出的步骤数
                    # 说明第 idx+2 行的数据执行通过，写入通过信息
                    writeTestResult(sheetObj=dataSourceSheetObj,
                                    rowNo = idx +2,colsNo = "dataSheet",
                                    testResult="pass")
                else:
                    # 写入失败信息
                    writeTestResult(sheetObj=dataSourceSheetObj,
                                    rowNo=idx+2,colsNo="dataSheet",
                                    testResult="faild")
        if requireDatas == successDatas:
            # 只有当成功的数据条数等于被设置为需要执行的数
            # 目，才能说明数据驱动测试通过
            return 1
        else:
            return 0
    except Exception as e:
        raise e


def TestKeyword(caseName,caseStepSheetName,idx):
    try:
        caseSheet = excelObj.getSheetByName(caseName)
        stepSheet = excelObj.getSheetByName(caseStepSheetName)

        # 获取步骤sheet中步骤数
        stepNum = excelObj.getRowsNumber(stepSheet)
        # print(stepNum)
        successfulSteps = 0
        # 记录测试用例i的步骤成功数
        logging.info("开始执行用例--[%s]"% caseName)
        for step in range(2,stepNum + 1):
            # 因为步骤sheet第一行为标题行，无须执行
            # 获取步骤sheet中第step行对象
            stepRow = excelObj.getRow(stepSheet,step)
            # 获取关键字作为调用的函数名
            keyWord = stepRow[testStep_keyWords - 1].value
            # 获取操作元素的定位方式作为调用函数的参数
            locationType = stepRow[testStep_locationType -1].value
            # 获取操作元素的定位表达式作为调用函数的参数
            locatorExpression = stepRow[testStep_locatorExpression -1].value
            # 获取操作值作为调用函数的参数
            operateValue = stepRow[testStep_operateValue -1].value

            # 将操作为数字类型的数据转化字符串类型，方便字符串拼接
            if isinstance(operateValue,int):
                operateValue = str(operateValue)
            # print(keyWord,locationType,locatorExpression,operateValue)

            # 字符串的拼接
            expressionStr = ""
            # 构造需要执行的python语句
            # 对应的PageAction.py文件中的页面动作函数调用的字符串表示
            if keyWord and operateValue and \
                locationType is None and locatorExpression is None:
                expressionStr = keyWord.strip()+"('"+operateValue+"')"
            elif keyWord and operateValue is None and \
                locationType is None and locatorExpression is None:
                expressionStr = keyWord.strip() + "()"
            elif keyWord and locationType and operateValue \
                and locatorExpression is None:
                expressionStr = keyWord.strip()+\
                    "('"+locationType.strip()+"','"+operateValue+"')"
            elif keyWord and locationType and locatorExpression and \
                operateValue:
                expressionStr = keyWord.strip()+\
                    "('"+locationType.strip()+"','"+\
                    locatorExpression.replace("'",'""').strip()+\
                    "','"+ operateValue+"')"
            elif keyWord and locationType and locatorExpression \
                and operateValue is None:
                expressionStr = keyWord.strip() + \
                                "('" + locationType.strip() + "','" + \
                                locatorExpression.replace("'", '""').strip() + "')"

            # print(expressionStr)
            try:
                # 通过eval函数，将拼接的页面动作函数调用字符串表示
                # 当成有效的Python表达式执行，从而执行测试步骤的sheet中
                eval(expressionStr)

                # 在测试执行时间写入列
                excelObj.writeCellCurrentTime(stepSheet,rowNo=step,
                                              colsNo=testStep_runTime)

            except Exception as e:
                # 获取异常屏幕图片
                capturePic = getScreenShot(caseStepSheetName)
                # 获取详细的异常堆栈信息
                errorInfo = traceback.format_exc()
                # 在测试步骤sheet中写入失败信息
                writeTestResult(stepSheet,step,"caseStep","faild",errorInfo,capturePic)

                logging.info("用例[%s]-[%s]步骤%d[%s]执行失败" % \
                             (caseName,caseStepSheetName,step-1,stepRow[testStep_testStepDescribe -1 ].value) )

            else:
                # 在测试步骤Sheet中写入成功信息
                writeTestResult(stepSheet,step,"caseStep","pass")
                # 每成功一步，successfulSteps变量自增1
                successfulSteps +=1
                logging.info("用例[%s]-[%s]步骤%d[%s]执行通过" % \
                             (caseName,caseStepSheetName,step-1,stepRow[testStep_testStepDescribe -1 ].value) )
        if successfulSteps == stepNum -1:
            # 当测试用例步骤sheet中所有步骤都执行成功
            # 此测试用例执行通过，然后将成功信息写入 测试用例工作表中
            writeTestResult(caseSheet,idx+2,"testCase","pass")

            return 1
        else:
            writeTestResult(caseSheet,idx+2,"testCase","faild")
            return 0

    except Exception as e:
        # 打印详细的异常堆栈信息
        print(traceback.print_exc())

if __name__ == "__main__":
    caseSheet = excelObj.getSheetByName("登入名和密码")
    caseStepName = "登录"

    dataDriverFun(caseSheet,caseStepName)