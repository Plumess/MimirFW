from pathlib import Path


def search_file_upwards(
    base_dir_path: Path,
    target_file_name: str,
    max_search_parent_depth: int,
) -> Path:
    """
    在当前目录或其父目录中向上搜索目标文件，直到指定深度。

    :param base_dir_path: 开始搜索的目录路径
    :param target_file_name: 要搜索的文件名
    :param max_search_parent_depth: 向上搜索的最大父目录层数
    :return: 如果找到文件则返回文件路径，否则抛出异常
    """
    current_path = base_dir_path.resolve()
    for _ in range(max_search_parent_depth):
        candidate_path = current_path / target_file_name
        if candidate_path.is_file():
            return candidate_path
        parent_path = current_path.parent
        if parent_path == current_path:  # 到达根目录
            break
        else:
            current_path = parent_path

    raise ValueError(
        f"在目录 '{base_dir_path.resolve()}' 或其父目录中未找到文件 '{target_file_name}'"
        f"，搜索深度为 {max_search_parent_depth}。"
    )
