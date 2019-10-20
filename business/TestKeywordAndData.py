from business.TestWriteDataExcel import *

# # 创建解析Excel对象
# excelObj = ParseExcel()
#
# # 将Excel数据文件加载到内存
# excelObj.loadWorkBook(dataFilePath)

def TestKeywordAndData():
    try:
        # 根据Excel文件中的sheet名称获取sheet对象
        caseSheet = excelObj.getSheetByName("测试用例")
        # 获取测试用例sheet中是否执行列对象
        isExecuteColumn = excelObj.getColumn(caseSheet, testCase_isExecute)
        # 记录执行成功的测试用例个数
        successfulCase = 0
        # 记录需要执行的用例个数
        requiredCase = 0

        for idx, i in enumerate(isExecuteColumn[1:]):  # idx默认从0开始， excel 表格行从1开始,列从1开始
            # 用例sheet中第一行为标题，无须执行
            caseName = excelObj.getCellOfValue(
                caseSheet,rowNo=idx+2,colsNo=testCase_testCaseName
            )
            # 循环遍历“测试用例”表中的测试用例，执行被设置为执行的用例
            # print(i.value)
            if i.value.lower() == "y":
                requiredCase += 1

                # 获取用例执行框架类型
                useFrameWorkName = excelObj.getCellOfValue(
                    caseSheet,rowNo=idx+2,
                    colsNo = testCase_frameWorkName
                )
                # 获取测试用例表中，第idx+1行中执行用例的步骤sheet名
                stepSheetName = excelObj.getCellOfValue(
                    caseSheet,rowNo=idx+2,
                    colsNo=testCase_testStepSheetName
                )
                logging.info("用例[%s]-步骤名[%s]-框架类型[%s]" % (caseName,stepSheetName,useFrameWorkName))

                if useFrameWorkName == "数据":
                    logging.info("********调用数据驱动********")
                    # 获取测试用例表中，第idx+1行，执行框架
                    # 数据驱动所使用的数据名
                    dataSheetName = excelObj.getCellOfValue(
                        caseSheet,rowNo=idx+2,
                        colsNo=testCase_dataSourceSheetName)
                    # 获取第idx+1行测试用例的步骤sheet对象
                    stepSheetObj = excelObj.getSheetByName(stepSheetName)
                    # 获取第idx+1行测试用例使用的数据sheet对象
                    dataSheetObj = excelObj.getSheetByName(dataSheetName)

                    # 通过数据驱动框架执行添加联系人
                    result = dataDriverFun(dataSheetObj,stepSheetName)
                    if result:
                        logging.info("用例[%s]执行成功" % caseName)
                        successfulCase += 1
                        writeTestResult(caseSheet,rowNo=idx+2,
                                        colsNo="testCase",
                                        testResult="pass")
                    else:
                        logging.info("用例[%s]执行失败" % caseName)
                        writeTestResult(caseSheet,rowNo=idx+2,
                                        colsNo="testCase",
                                        testResult="faild")

                elif useFrameWorkName == "关键字":
                    logging.info("********调用关键字驱动********")
                    result_keyword = TestKeyword(caseName,stepSheetName,idx)
                    if result_keyword:
                        logging.info("用例[%s]执行成功" % caseName)
                        successfulCase += 1
                        writeTestResult(caseSheet,rowNo=idx+2,
                                        colsNo="testCase",
                                        testResult="pass")
                    else:
                        logging.info("用例[%s]执行失败" % caseName)
                        writeTestResult(caseSheet, rowNo=idx + 2,
                                        colsNo="testCase",
                                        testResult="faild")

        logging.info("共%d条用例，%d条需要被执行，本次执行通过%d条" \
                 % (len(isExecuteColumn) - 1, requiredCase, successfulCase))
    except Exception as e:
        print(traceback.print_exc())

if __name__ == "__main__":
    TestKeywordAndData()