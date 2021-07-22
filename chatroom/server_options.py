from dataclasses import dataclass


@dataclass(frozen=True)
class SeverOptions:

    CHGRP: int = 0
    ADDGRP: int = 1
    CHGID: int = 2
    DELGRP: int = 3
    ALLUSR: int = 4
    
