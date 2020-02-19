


class Loader(object):
    """
    Un Loader.
    """

    def __init__(self, container=None, description=None):

        if container is not None and isinstance(container, list):
            self.__container = container
        else:
            self.__container = None

        if description is not None and isinstance(description, str):
            self.__description = description
        else:
            self.__description = None


    @property
    def container(self):
        """
        Regresa los contenidos de el loader
        """
        if self.__container:
            return self.__container


    @container.setter
    def container(self, value):
        """
        Recarga el Loader
        """
        if isinstance(value, list):
            self.__container = value
        else:
            raise Exception("New container value must be type list")


    @container.deleter
    def container(self):
        """
        No borra la propiedad, settea a nada
        """
        if self.__container:
            self.__container = None


    @property
    def description(self):
        if self.__description:
            return self.__description


    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self.__description = value
        else:
            raise NotImplemented("Descirption must be type string")


    @description.deleter
    def description(self):
        """
        Does not delete, it just sets to None
        """
        if self.__description:
            self.__description = None


    def __iter__(self):
        """
        Regresa los contenidos de loader como iterador
        """
        if self.__container:
            return iter([o_o for o_o in self.__container])


    def __str__(self):
        """
        Custom reprs
        """
        if self.description:
            return super().__str__() + " " + self.description
        else:
            return super().__str__()
        
        