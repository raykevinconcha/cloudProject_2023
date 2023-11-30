
# models.py
from pydantic import BaseModel
from typing import List

class RolBase(BaseModel):
    name_rol: str

class RolCreate(RolBase):
    pass

class Rol(RolBase):
    idroldID: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name_user: str
    username: str
    password: str
    roldID_idroldID: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    idUsers: int
    roldID: Rol

    class Config:
        from_attributes = True

class LogsBase(BaseModel):
    log_activityType: str
    log_Timestamp: str
    Users_idUsers: int

class LogsCreate(LogsBase):
    pass

class Logs(LogsBase):
    idLogs: int
    user: User

    class Config:
        from_attributes = True

class TopologyBase(BaseModel):
    name_topology: str

class TopologyCreate(TopologyBase):
    pass

class Topology(TopologyBase):
    idTopology: int

    class Config:
        from_attributes = True

class SlicesBase(BaseModel):
    name: str
    status: str
    number_nodes: str
    number_links: str
    Users_idUsers: str
    Topology_idTopology: int

class SlicesCreate(SlicesBase):
    pass

class Slices(SlicesBase):
    idSlices: int
    user: User
    topology: Topology

    class Config:
        from_attributes = True

class TokenBase(BaseModel):
    Slices_idSlices: int
    TokenValue: str

class TokenCreate(TokenBase):
    pass

class Token(TokenBase):
    idToken: int
    slices: Slices

    class Config:
        from_attributes = True

class VMImagesBase(BaseModel):
    name: str
    Slices_idSlices: int

class VMImagesCreate(VMImagesBase):
    pass

class VMImages(VMImagesBase):
    idVM_images: int
    slices: Slices

    class Config:
        from_attributes = True

class NodesBase(BaseModel):
    VM_name: str
    capacity: str
    port: str
    description: str
    Slices_idSlices: int
    VM_images_idVM_images: int

class NodesCreate(NodesBase):
    pass

class Nodes(NodesBase):
    idNodes: int
    slices: Slices
    vm_images: VMImages

    class Config:
        from_attributes = True

class SystemsResourcesBase(BaseModel):
    ResourceUsage: str
    Slices_idSlices: int

class SystemsResourcesCreate(SystemsResourcesBase):
    pass

class SystemsResources(SystemsResourcesBase):
    idsytemsresources: int
    slices: Slices

    class Config:
        from_attributes = True

class VMConfigurationsBase(BaseModel):
    VMName: str
    Slices_idSlices: int
    MemorySize: str

class VMConfigurationsCreate(VMConfigurationsBase):
    pass

class VMConfigurations(VMConfigurationsBase):
    idVMConfigurations: int
    slices: Slices

    class Config:
        from_attributes = True
