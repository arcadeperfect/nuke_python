# from file_system import check_dir
from ..util.error_frames import *
import nuke
import os
from enum import Enum, auto


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

    
        


        
      
class PathComponent(Enum):
    DIRNAME = auto()
    SEQNAME = auto()
    EXT = auto()
     
        
def split_sequence(seq):
    dirname = os.path.dirname(seq)
    basename = os.path.basename(seq)
    seqname = basename.split('.')[0:-2]
    ext = basename.split('.')[-1]
    
    return {
        PathComponent.DIRNAME: dirname,
        PathComponent.SEQNAME: seqname,
        PathComponent.EXT: ext
    }