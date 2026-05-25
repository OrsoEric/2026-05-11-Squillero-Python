"""
python excercise_lib_pympler.py 
Size of my_class: 0 bytes
(.venv) sona@rpi-orso-sdb:~/2026-05-11-Squillero-Python$ python excercise_lib_pympler.py 
Traceback (most recent call last):
  File "/home/sona/2026-05-11-Squillero-Python/excercise_lib_pympler.py", line 8, in size
    from pympler import asizeof
ModuleNotFoundError: No module named 'pympler'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/sona/2026-05-11-Squillero-Python/excercise_lib_pympler.py", line 18, in <module>
    print(f"Size of my_class: {my_class.size} bytes")
                               ^^^^^^^^^^^^^
  File "/home/sona/2026-05-11-Squillero-Python/excercise_lib_pympler.py", line 11, in size
    raise ImportError("Pympler library is not installed. Please install it using 'pip install pympler' to use the size property.")
ImportError: Pympler library is not installed. Please install it using 'pip install pympler' to use the size property.
(.venv) sona@rpi-orso-sdb:~/2026-05-11-Squillero-Python$ uv pip install pympler
Resolved 1 package in 583ms
Prepared 1 package in 197ms
Installed 1 package in 18ms
 + pympler==1.1
(.venv) sona@rpi-orso-sdb:~/2026-05-11-Squillero-Python$ python 
excercise_lib_pympler.py 
Size of my_class: 40448 bytes



"""



class Cl_my_class:
    def __init__(self):
        self.g_ln = list(range(1000))

    @property
    def size(self) -> int:
        try:
            from pympler import asizeof
            return asizeof.asizeof(self)    
        except ImportError:
            raise ImportError("Pympler library is not installed. Please install it using 'pip install pympler' to use the size property.")
            return 0
        return 0


if __name__ == "__main__":
    my_class = Cl_my_class()
    print(f"Size of my_class: {my_class.size} bytes")



