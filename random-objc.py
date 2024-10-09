
import random
import string
import os

# 当前文件目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 关键字配置文件
KEYWORDS_FILE = CURRENT_DIR + "/keywords.txt"

# 类前缀
CLASS_PRE = "Test"

# 随机生成多少个类文件
FILE_NUM = 100

# 文件导出目录
OUTPUT = CURRENT_DIR + "/output/" + CLASS_PRE


void = 0
NSString = 1
NSInteger = 3
NSNumber = 4
BOOL = 5
double = 6
NSArray = 2
NSDictionary = 7
UIView = 8
UIFont = 9

def objc_type_name(type):
    if type == void:
        return "void"
    if type == NSString:
        return "NSString *"
    if type == NSInteger:
        return "NSInteger "
    if type == NSNumber:
        return "NSNumber *"
    if type == BOOL:
        return "BOOL "
    if type == double:
        return "double "
    if type == NSArray:
        return "NSArray *"
    if type == NSDictionary:
        return "NSDictionary *"
    if type == UIView:
        return "UIView *"
    if type == UIFont:
        return "UIFont *"
        
        
def random_objc_property_value(type):
    if type == void:
        return ""
    if type == NSString:
        v = f"{random_keywords()}{str(random.randint(0, 10000))}{random_keywords()}"
        return f"@\"{v}\""
    if type == NSArray:
        return "@[]"
    if type == NSInteger:
        return str(random.randint(0, 10000))
    if type == NSNumber:
        return f"@{random.randint(0, 10000)}"
    if type == BOOL:
        return "YES" if random.randint(0, 1) == 1 else "NO"
    if type == double:
        return str(random.randint(0, 10000))
    if type == NSDictionary:
        return "@{}"
    if type == UIView:
        return "[UIView new]"
    if type == UIFont:
        return f"[UIFont systemFontOfSize:{random.randint(9, 30)}]"
    return "nil"


class ObjcProperty:
    def __init__(self):
        self.name = ""
        self.type = 0
        self.ref = ""
        self.typename = "NSString *"
        
    def Random():
        result = ObjcProperty()
        
        name = random_keywords()
        if random.random() < 0.1:
            name = f"{name}_{random_keywords()}"
        if random.random() < 0.1:
            name = f"{name}_{random_keywords()}"
        if random.random() < 0.1:
            name = f"{name}_{random_keywords()}"
        name = underscore_to_camelcase(name,True)
        
        result.name = name
        result.type = random.randint(1, 9)
        result.typename = objc_type_name(result.type)
        if result.type == NSString:
            result.ref = "strong"
        if result.type == NSInteger:
            result.ref = "assign"
        if result.type == NSArray:
            result.ref = "strong"
        if result.type == NSNumber:
            result.ref = "strong"
        if result.type == BOOL:
            result.ref = "assign"
        if result.type == double:
            result.ref = "assign"
        if result.type == NSDictionary:
            result.ref = "strong"
        if result.type == UIView:
            result.ref = "strong"
        if result.type == UIFont:
            result.ref = "strong"
        return result


class ObjcFunc:
    def __init__(self):
        self.name = ""
        self.type = 0
        self.returntype = 0
        self.params = [] # ObjcProperty
        self.fullname = ""
        self.run = ""
        
    def Random():
        result = ObjcFunc()
        name = random_keywords()
        name = f"{name}_{random_keywords()}"
        name = f"{name}_{random_keywords()}"
        if random.random() < 0.3:
            name = f"{name}_{random_keywords()}"
        if random.random() < 0.6:
            name = f"{name}_{random_keywords()}"
        if random.random() < 0.9:
            name = f"{name}_{random_keywords()}"
        name = underscore_to_camelcase(name,True)
        result.name = name
        for i in range(0, random.randint(0, 5)):
            result.params.append(ObjcProperty.Random())
        result.type = random.randint(0, 1)
        result.returntype = random.randint(0, 8)
        fullname = ""
        if result.type == 0:
            fullname = f"{fullname}- "
        if result.type == 1:
            fullname = f"{fullname}+ "
        fullname = f"{fullname}({objc_type_name(result.returntype).rstrip()})"
        fullname = f"{fullname}{result.name}"
        for i in range(0 ,len(result.params)):
            p = result.params[i]
            typename = p.typename.rstrip()
            if i == 0:
                fullname = f"{fullname}:({typename}){p.name} "
            else:
                fullname = f"{fullname}{p.name}:({typename}){p.name} "
        fullname = fullname.rstrip()
        result.fullname = fullname
        return result


class ObjcClass:
    def __init__(self):
        self.name = ""
        self.supertype = 0
        self.supername = "NSObject"
        self.importH = "#import <UIKit/UIKit.h>"
        self.func = []
        self.property = []
        self.output = ""
        self.link = [] # ObjcClass
        
    def contains_property(self,property):
        for obj in self.property:
            if obj.name == property.name:
                return True
        return False
    
    def Random():
        result = ObjcClass()
        result.name = random_class_name()
        for i in range(0, random.randint(0, 30)):
            p = ObjcProperty.Random()
            if result.contains_property(p) == False:
                result.property.append(p)
        for i in range(0, random.randint(0, 30)):
            result.func.append(ObjcFunc.Random())
        result.supertype = random.randint(0, 2)
        if result.supertype == 0:
            result.supername = "NSObject"
            result.importH = "#import <UIKit/UIKit.h>"
        if result.supertype == 1:
            result.supername = "UIViewController"
            result.importH = "#import <UIKit/UIKit.h>"
        if result.supertype == 2:
            result.supername = "UIView"
            result.importH = "#import <UIKit/UIKit.h>"
        result.output = OUTPUT
        return result
        
    def export(self):
        # 生成 .h 文件
        self.exportH()
        # 生成 .m 文件
        self.exportM()
        
    def exportH(self):
        code = ""
        code = random_enter_for(code)
        code = f"{code}{self.importH}\n"
        code = f"{code}\n"
        code = f"{code}NS_ASSUME_NONNULL_BEGIN\n\n"
        code = random_enter_for(code)
        code = f"{code}@interface {self.name} : {self.supername}\n"
        code = random_enter_for(code)
        for p in self.property:
            code = f"{code}@property ({p.ref} ,nonatomic) {p.typename}{p.name};\n"
            code = random_enter_for(code)
        code = f"{code}\n"
        code = random_enter_for(code)
        code = random_enter_for(code)
        for f in self.func:
            code = f"{code}{f.fullname};\n"
            code = random_enter_for(code)
        code = f"{code}@end\n\n"
        code = f"{code}NS_ASSUME_NONNULL_END"
        code = random_enter_for(code)
        file = open(f"{self.output}/{self.name}.h", "w")
        file.write(code)
        file.close()
        
    def exportM(self):
        code = ""
        code = random_enter_for(code)
        code = f"{code}#import \"{self.name}.h\"\n"
        for obj in self.link:
            if obj.name != self.name:
                code = f"{code}#import \"{obj.name}.h\"\n"
        
        code = f"{code}\n"
        code = random_enter_for(code)
        code = f"{code}@implementation {self.name}\n"
        code = random_enter_for(code)
        
        code = f"{code}- (instancetype)init {{\n"
        code = f"{code}    self = [super init];\n"
        code = f"{code}    if (self) {{\n"
        
        for p in self.property:
            code = f"{code}        _{p.name} = {random_objc_property_value(p.type)};\n"
            code = random_enter_for(code)
            
        for obj in self.func:
            sender = "self" if obj.type == 0 else self.name
            full_run_func = f"{sender} {obj.name}"
            for i in range(0 ,len(obj.params)):
                p = obj.params[i]
                if i == 0:
                    full_run_func = f"{full_run_func}:{random_objc_property_value(p.type)} "
                else:
                    full_run_func = f"{full_run_func}{p.name}:{random_objc_property_value(p.type)} "
            full_run_func = full_run_func.rstrip()
            code = f"{code}        [{full_run_func}];\n"
            code = random_enter_for(code)
        
        code = f"{code}    }} return self;\n"
        code = f"{code}}}\n\n"
        code = random_enter_for(code)
        
        for obj in self.func:
            if obj.returntype == void:
                code = f"{code}{obj.fullname} {{\n\n}}\n"
            else:
                code = f"{code}{obj.fullname} {{\n    return {random_objc_property_value(obj.returntype)};\n}}\n"
        
        code = f"{code}@end\n"
        file = open(f"{self.output}/{self.name}.m", "w")
        file.write(code)
        file.close()
        
    def random_func_from_link(self):
        obj = random.choice(self.link)
        return random.choice(obj.func)
        
        
# 生成随机类名
def random_class_name():
    result = ""
    result = f"{result}_{random_keywords()}"
    if random.random() < 0.8:
        result = f"{result}_{random_keywords()}"
    if random.random() < 0.4:
        result = f"{result}_{random_keywords()}"
    if random.random() < 0.2:
        result = f"{result}_{random_keywords()}"
    if random.random() < 0.3:
        result = f"{result}_controller"
    result = underscore_to_camelcase(result)
    result = f"{random_pre()}{result}"
    return result
    
# 类前缀
def random_pre():
    return CLASS_PRE

# 随机在尾部插入换行符
def random_enter_for(code):
    if random.random() < 0.2:
        code = f"{code}\n"
    return code
    
# 从 file 文件里随机读取一行文本
def random_keywords(file = KEYWORDS_FILE):
    result = ""
    with open(file, 'r', encoding='utf-8') as file:
        # 读取所有行
        lines = file.readlines()
        random_line = random.choice(lines)
        result = random_line.strip()
    if result == "":
        result = "".join(random.choices(string.ascii_uppercase, k=5))
    return result
    
# 下划线转驼峰
def underscore_to_camelcase(underscore_string,lowerFirst = False):
    words = underscore_string.split('_')
    camelcase_string = ''.join(word.capitalize() for word in words)
    if lowerFirst == True:
        camelcase_string = camelcase_string[0].lower() + camelcase_string[1:]
    return camelcase_string
    
    
# 清空目录下的所有文件
def clear(directory):
    # 获取目录中的所有文件
    files = os.listdir(directory)
    # 遍历并删除每个文件
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


def main():
    
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    clear(OUTPUT)
    
    # 一共生成多少个类
    total = FILE_NUM
    
    # 每个文件最多关联多少个类
    link = total if total < 20 else 20
    
    allObjcClass = []
    for i in range(0, total):
        obj = ObjcClass.Random()
        allObjcClass.append(obj)
        
    for obj in allObjcClass:
        obj.link = random.sample(allObjcClass, random.randint(0, link))
        
    for obj in allObjcClass:
        obj.export()
        
    code = ""
    for obj in allObjcClass:
        code = f"{code}#import \"{obj.name}.h\"\n"
    file = open(f"{OUTPUT}/{CLASS_PRE}Headers.h", "w")
    file.write(code)
    file.close()

if __name__ == "__main__":
    main()


