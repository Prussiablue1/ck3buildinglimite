import os


def remove_module_content(content, module_name):
    """
    删除指定模块（例如can_construct、is_enabled或can_construct_potential）及其内嵌内容
    """
    # 查找模块的位置
    pattern = rf'{module_name}\s*=\s*{{'
    start_index = 0

    while True:
        # 查找模块起始位置
        start_index = content.find(f'{module_name} = {{', start_index)
        if start_index == -1:
            break  # 如果没有找到更多模块，结束循环

        # 进入栈模式，寻找对应的结束括号
        stack = []
        end_index = start_index
        while end_index < len(content):
            if content[end_index] == '{':
                stack.append('{')
            elif content[end_index] == '}':
                stack.pop()
                if not stack:  # 如果栈为空，表示找到了完整的闭合括号
                    break
            end_index += 1

        # 删除整个模块内容
        content = content[:start_index] + f'{module_name} = {{}}' + content[end_index + 1:]

        # 继续查找下一个模块
        start_index = end_index

    return content


def process_file(input_filename, output_filename):
    try:
        # 读取原文件内容
        with open(input_filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # 删除can_construct、is_enabled和can_construct_potential模块的内容
        content = remove_module_content(content, 'can_construct')
        content = remove_module_content(content, 'is_enabled')
        #content = remove_module_content(content, 'can_construct_potential')

        # 将处理后的内容写入新文件
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"文件已成功处理并保存为 {output_filename}")
    except Exception as e:
        print(f"处理文件时出错: {e}")


def generate_output_filename(input_filename, output_dir):
    """
    根据输入文件路径生成输出文件路径，保持文件名不变，但输出到指定目录。
    """
    # 获取输入文件的文件名
    filename = os.path.basename(input_filename)

    # 生成输出文件路径
    output_filename = os.path.join(output_dir, filename)

    return output_filename


def process_all_files(input_dir, output_dir):
    """
    遍历输入目录中的所有.txt文件并处理，生成对应的输出文件到输出目录。
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有txt文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_dir, filename)
            output_file = generate_output_filename(input_file, output_dir)

            # 处理文件
            process_file(input_file, output_file)


# 使用示例
input_dir = 'back'  # 输入文件夹路径
output_dir = 'new'  # 输出文件夹路径
process_all_files(input_dir, output_dir)
