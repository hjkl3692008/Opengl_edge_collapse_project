import pandas as pd
import os
import struct
import numpy as np
from PIL import Image

from OpenGL.GL.EXT import texture_compression_s3tc


# get cwd
def get_cwd():
    return os.getcwd()


# join path
def join_path(*args):
    path = ''
    for v in args:
        path = os.path.join(path, v)
    return path


# root path.  os.path.pardir = ..
# basic_path = join_path(get_cwd(), os.path.pardir, 'resource')
basic_path = get_cwd()


# load table
def load_table(path, sep='\t', delim_whitespace=False, header='infer', skiprows=None, nrows=None):
    data = pd.read_csv(path, sep=sep, delim_whitespace=delim_whitespace, header=header, skiprows=skiprows, nrows=nrows)
    return data


# load shader file : vertex_shader and fragment_shader
def load_shader_file(vertex_shader_names, fragment_shader_names):
    assert isinstance(vertex_shader_names, list)
    assert isinstance(fragment_shader_names, list)
    vertex_shader_source_list = []
    fragment_shader_source_list = []
    for vsn in vertex_shader_names:
        vsn_path = join_path(basic_path, 'resource', 'shader', vsn)
        f = open(vsn_path, 'rb')
        vertex_shader_source_list.append(f.read())
        f.close()
    for fsn in fragment_shader_names:
        fsn_path = join_path(basic_path, 'resource', 'shader', fsn)
        f = open(fsn_path, 'rb')
        fragment_shader_source_list.append(f.read())
        f.close()
    return vertex_shader_source_list, fragment_shader_source_list


# load texture
TEXTURE_DDS = 'DDS'
TEXTURE_PNG = 'BMP'


def load_texture_file(texture_name, texture_type):
    file_path = join_path(basic_path, 'resource', 'texture', texture_name)
    if texture_type == TEXTURE_DDS:
        head, dds_buffer = load_dds_texture(file_path)
        return head, dds_buffer
    elif texture_type == TEXTURE_PNG:
        para_dict, buffer = load_png_texture(file_path)
        return para_dict, buffer


def load_dds_texture(file_path):
    f = open(file_path, 'rb')
    dds_tag = f.read(4)
    if dds_tag != b"DDS ":
        raise Exception("invalid dds file")
    head = f.read(124)
    linearSize, = struct.unpack("I", head[16:20])
    mipMapCount, = struct.unpack("I", head[24:28])
    fourCC = head[80:84]
    supported_DDS = [b"DXT1", b"DXT3", b"DXT5"]

    if fourCC not in supported_DDS:
        raise Exception("Not supported DDS file: %s" % fourCC)

    if mipMapCount > 1:
        bufferSize = linearSize * 2
    else:
        bufferSize = linearSize

    dds_buffer = f.read(bufferSize)
    f.close()
    return head, dds_buffer


def load_png_texture(file_path, mode='RGB'):
    image = Image.open(file_path)
    converted = image.convert(mode)
    buffer = converted.transpose(Image.FLIP_TOP_BOTTOM).tobytes()
    para_dict = {'height': image.height, 'width': image.width, 'mode': mode}
    image.close()
    return para_dict, buffer


# load_cow
def load_cow(trans=True):
    cow_path = join_path(basic_path, 'resource', 'object', 'cow.d.txt')
    head = pd.read_table(cow_path, header=None, nrows=1)
    point_num = head.iat[0, 1]
    polygon_num = head.iat[0, 2]
    points = pd.read_table(cow_path, header=None, skiprows=1, nrows=point_num)
    polygons = pd.read_table(cow_path, delim_whitespace=True, usecols=range(0, 7), header=None,
                             skiprows=(1 + point_num), nrows=polygon_num, keep_default_na=False, error_bad_lines=False)
    if trans:
        points = np.array(points)
        polygons = np.array(polygons)
    return head, points, polygons


# judge whether file exist
def is_exist(t, name):
    full_path = join_path(basic_path, t, name)
    flag = os.path.exists(full_path)
    return flag


# dataFrame to array
def df2np(data):
    return data.values
