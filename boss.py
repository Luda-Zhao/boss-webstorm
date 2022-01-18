from selenium import webdriver # 从selenium导入webdriver
import time
import csv

# BOSS爬虫类
class BuildBossSpider:
    def __init__(self):
        self.url="https://www.zhipin.com/"
        str=input("chromedriver的绝对路径\n")
        self.driver=webdriver.Chrome(executable_path=str)
    def search(self,str):
        '''
        搜索职位名
        :param str:
        :return:
        '''
        self.driver.get(self.url)
        input = self.driver.find_element_by_xpath('//*[@placeholder="搜索职位、公司"]')
        input.send_keys(str)  # 输入搜索关键词
        self.driver.find_element_by_xpath('//*[@ka="search_box_index"]').click()  # 点击搜索按钮
        print("等待页面加载中")
        time.sleep(5)
    def printitems(self):
        '''
        打印职位列表
        :return:
        '''
        salarys = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[2]/span')
        jobs = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[1]/span[1]/a')
        locates = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[1]/span[2]/span')
        companys = self.driver.find_elements_by_xpath('//*[@class="info-company"]/div/h3/a')
        requirements = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[2]/p')
        for salary, job, locate, company, requirement in zip(salarys, jobs, locates, companys, requirements):
            print(job.text.replace('\n', ','), salary.text.replace('\n', ','), company.text.replace('\n', ','),
                  locate.text.replace('\n', ','), requirement.text)
    def savedata(self,str):
        '''
        保存至文件
        :param str:
        :return:
        '''
        salarys = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[2]/span')
        jobs = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[1]/span[1]/a')
        locates = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[1]/span[2]/span')
        companys = self.driver.find_elements_by_xpath('//*[@class="info-company"]/div/h3/a')
        requirements = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[2]/p')
        ans=[]
        for salary, job, locate, company, requirement in zip(salarys, jobs, locates, companys, requirements):
            tem=[job.text,salary.text,company.text,locate.text,requirement.text]
            ans.append(tem)
        with open("boss"+str+".csv","w") as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(["职位","薪资","公司","所在地","要求"])
            writer.writerows(ans)
        print("文件已保存到boss"+str+".csv")
    def SaveOnePageData(self,ans):
        '''
        爬取一个页面中的列表
        :param ans:
        :return:
        '''
        salarys = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[2]/span')
        jobs = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[1]/span[1]/a')
        locates = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[1]/span[2]/span')
        companys = self.driver.find_elements_by_xpath('//*[@class="info-company"]/div/h3/a')
        requirements = self.driver.find_elements_by_xpath('//*[@class="primary-wrapper"]/div/div[2]/p')
        for salary, job, locate, company, requirement in zip(salarys, jobs, locates, companys, requirements):
            tem=[job.text,salary.text,company.text,locate.text,requirement.text]
            ans.append(tem)
        return ans
    def savetofile(self,ans,str):
        '''
        保存至文件
        :param ans:
        :param str:
        :return:
        '''
        with open("boss"+str+".csv","w") as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(["职位","薪资","公司","所在地","要求"])
            writer.writerows(ans)
        print("文件已保存到boss"+str+".csv")
    def nextPage(self):
        '''
        翻页
        :return:
        '''
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@class="next"]').click()


    def run(self):
        '''
        运行代码
        :return:
        '''
        str=input("请输入职位名\n")
        self.search(str)
        ans=[]
        ans = self.SaveOnePageData(ans)
        while True:
            try:
                self.nextPage()
                ans=self.SaveOnePageData(ans)
            except BaseException:
                break
        self.savetofile(ans,str)
        #self.driver.quit()

if __name__=="__main__":
    spider = BuildBossSpider()
    while True:
        try:
            spider.run()
        except BaseException:
            print("进程结束")
            spider.driver.quit()
            break
