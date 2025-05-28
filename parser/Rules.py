class Rules:
    def __init__(self):
        self.rules = {
            0: ["WORLDNAME", "<id>", "COLON", "<programa>"],
            1: ["IDENTIFIER"],
        
            2: ["<seccion_de_constantes>", "<punto_entrada_del_programa>", "WORLDSAVE"],
            
            3: ["BEDROCK", "<constantes>"],
            4: [],
            5: ["<constante>", "<constantes>"],
            6: [],
            7: ["OBSIDIAN", "<tipo>", "<id>", "<literal>"],
        
            8: ["SPAWNPOINT", "<cuerpo_rutina>"],
        
            9: ["POLLOCRUDO", "<instrucciones>", "POLLOASADO"],

            10: ["<instruccion>", "<instrucciones>"],
            11: [],
            
            12: ["STACK"],
            13: ["RUNE"],
            14: ["SPIDER"],
            15: ["TORCH"],
            16: ["GHAST"],

            17: ["STRING"],
            18: ["CHAR"],
            19: ["INTEGER"],
            20: ["FLOAT"],
            21: ["ON"],
            22: ["OFF"],

            23: ["CREEPER"]
        }
        
    def getRules(self):
        return self.rules

