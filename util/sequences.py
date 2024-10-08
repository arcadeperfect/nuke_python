# from file_system import check_dir
from ..util.error_frames import *
import nuke
import os
import re
from pathlib import Path
from enum import Enum, auto
from collections import defaultdict

class FileSeq:
    
    class Status(Enum):
        Unvalidated = auto()
        No_files_found = auto()
        Some_files_missing = auto()
        All_files_found = auto()
        Error = auto()
     
     
    
    def __init__(self, dirname, seqname, ext, first, last):
        self.dirname = dirname
        self.seqname = seqname
        self.ext = ext
        self.first = first
        self.last = last
        self.good_frames = None
        self.missing_frames = None
        self.Status = FileSeq.Status.Unvalidated
        self.node = None
        self.file_names = None
        
    @classmethod
    def fromNode(cls, node):
        if isinstance(node, nuke.Node):
            if "file" in node.knobs().keys():
                path = node['file'].getValue()
                
                components = split_sequence(path)
                
                dirname = components[PathComponent.DIRNAME]
                seqname = components[PathComponent.SEQNAME]
                ext = components[PathComponent.EXT]
                
                result = cls(dirname, seqname, ext, node['first'].value(), node['last'].value())
                result.node = node
                return result
            else:
                raise TypeError("expect a node with a 'file' knob")
        else:
            raise TypeError("expect a node")
        
        
    def check_files(self):
        
        print(type(self.dirname))
        print(type(self.seqname))
        print(type(self.ext))
        
        found = list_sequence_files(self.dirname, self.seqname, self.ext)
        return found
        
        
            
        
    def validate(self):
                    
        expected_length = abs(self.first - self.last)
        
        if self.node:
            self.good_frames = getGoodFramesFromReadNode(self.node)
            self.missing_frames = getErrorFramesFromReadNode(self.node)
            
            if len(self.good_frames) == expected_length:
                self.Status = FileSeq.Status.All_files_found
            if len(self.good_frames) > expected_length:
                self.Status = FileSeq.Status.Error
            if len(self.good_frames) < expected_length and self.missing_frames.count() > 0:
                self.Status = FileSeq.Status.Some_files_missing
            if len(self.good_frames) == 0:
                self.Status = FileSeq.Status.No_files_found
                
            print(self.Status)
            
        else:
            raise NotImplementedError("validation is only implemented for FileSeqs with an associated Read node")
        
    def check_padding(self):
        min_padding = len(str(self.last))
        
        
    
        
        

    def get_file_list(self):
        file_list = []
        
        for i in range(self.first, self.last):
            file_list.append(os.path.join(self.dirname, self.seqname + '.' + str(i) + '.' + self.ext))
        
        return file_list
        


        
      
class PathComponent(Enum):
    DIRNAME = auto()
    SEQNAME = auto()
    EXT = auto()
     
        
def split_sequence(seq):
    dirname = os.path.dirname(seq)
    basename = os.path.basename(seq)
    seqname = ".".join(basename.split('.')[0:-2])
    ext = basename.split('.')[-1]
    
    return {
        PathComponent.DIRNAME: dirname,
        PathComponent.SEQNAME: seqname,
        PathComponent.EXT: ext
    }
  
  
  
def list_sequence_files(directory, sequence_name, extension):
    """
    Lists all files in the given directory that match the given sequence name and extension.
    """
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # Compile a regex pattern to match the specific sequence with varying padding
    pattern = rf'^{re.escape(sequence_name)}\.(\d+){re.escape(extension)}$'
    regex = re.compile(pattern)
    
    sequence_files = []
    
    # Iterate through all files in the directory
    for file_path in Path(directory).iterdir():
        if file_path.is_file():
            # print(f"Checking: {file_path.name}   :::   {sequence_name}")
            match = regex.match(file_path.name)
            if match:
                frame_number = int(match.group(1))  # Extract the frame number
                sequence_files.append(str(file_path))
                print(f"Matched: {file_path.name} (Frame: {frame_number})")
         
    return sequence_files  
