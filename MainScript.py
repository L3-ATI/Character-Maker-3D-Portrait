import bpy

import bpy

import bpy

import bpy

def update_ears(self, context):
    """Met à jour l'oreille et les boucles d'oreilles en fonction des choix sélectionnés."""
    
    obj = bpy.data.objects.get("head")  # Récupérer l'objet 'head'
    
    if not obj:
        print("L'objet 'head' n'existe pas !")
        return
    
    # Vérifier s'il y a un modificateur Boolean
    bool_modifier = next((mod for mod in obj.modifiers if mod.type == 'BOOLEAN'), None)
    
    if not bool_modifier:
        print("Aucun modificateur Boolean trouvé sur 'head'.")
        return
    
    # Associer l'oreille sélectionnée à un objet
    ear_objects = {
        "human": "boolEars1",
        "elfe": "boolEars2",
        "fae": "boolEars3"
    }
    
    selected_ear = ear_objects.get(self.ear_type)

    if selected_ear:
        ear_obj = bpy.data.objects.get(selected_ear)
        if ear_obj:
            bool_modifier.object = ear_obj
            print(f"Modificateur Boolean mis à jour avec {selected_ear}.")
        else:
            print(f"L'objet {selected_ear} n'existe pas dans la scène.")
    
    # --- Mise à jour des boucles d'oreilles ---
    
    # Associer le bon modèle de boucle d'oreille en fonction du type d'oreille
    earring_objects = {
        "human": {
            "stud": ("studEarrings_L1", "studEarrings_R1"),
            "hoop": ("hoopEarrings_L1", "hoopEarrings_R1"),
            "drop": ("dropEarrings_L1", "dropEarrings_R1")
        },
        "elfe": {
            "stud": ("studEarrings_L2", "studEarrings_R2"),
            "hoop": ("hoopEarrings_L2", "hoopEarrings_R2"),
            "drop": ("dropEarrings_L2", "dropEarrings_R2")
        },
        "fae": {
            "stud": ("studEarrings_L3", "studEarrings_R3"),
            "hoop": ("hoopEarrings_L3", "hoopEarrings_R3"),
            "drop": ("dropEarrings_L3", "dropEarrings_R3")
        }
    }
    
    # Désactiver toutes les boucles d'oreilles avant d'afficher les nouvelles
    for obj in bpy.data.objects:
        if "Earrings_L" in obj.name or "Earrings_R" in obj.name:
            obj.hide_set(True)

    # Récupérer les boucles d'oreilles correspondantes
    selected_earrings = earring_objects.get(self.ear_type, {}).get(self.earrings_L)  # Utilisation de earrings_L pour choisir le modèle
    
    if selected_earrings:
        left_earring, right_earring = selected_earrings  # Décomposer en boucle gauche et droite

        # Activer la boucle d'oreille gauche
        earring_obj_L = bpy.data.objects.get(left_earring)
        if earring_obj_L:
            earring_obj_L.hide_set(False)
            print(f"Boucle d'oreille gauche activée : {left_earring}.")
        else:
            print(f"L'objet {left_earring} n'existe pas dans la scène.")

        # Activer la boucle d'oreille droite
        earring_obj_R = bpy.data.objects.get(right_earring)
        if earring_obj_R:
            earring_obj_R.hide_set(False)
            print(f"Boucle d'oreille droite activée : {right_earring}.")
        else:
            print(f"L'objet {right_earring} n'existe pas dans la scène.")




def update_facial_shape_keys(self, context):
    """ Met à jour les shape keys du visage et des yeux en même temps. """
    head = bpy.data.objects.get("head")
    eyes = bpy.data.objects.get("eyes")
    
    # Sélectionner les sourcils actifs
    brows_objects = {
        "eyebrows1": bpy.data.objects.get("eyebrows1"),
        "eyebrows2": bpy.data.objects.get("eyebrows2"),
        "eyebrows3": bpy.data.objects.get("eyebrows3"),
    }
    
    active_brows = brows_objects.get(self.brows_type)
        
    if not head or not head.data.shape_keys:
        print("L'objet 'head' n'a pas de shape keys !")
        return

    if not eyes or not eyes.data.shape_keys:
        print("L'objet 'eyes' n'a pas de shape keys !")
        return
    
    if not active_brows or not active_brows.data.shape_keys:
        print("L'objet 'eyebrows' n'a pas de shape keys !")
        return

    # Shape keys associées
    shape_keys = {
        
        "brows_height": self.brows_height,
        "brows_depth": self.brows_depth,
        
        "eyes_proximity": self.eyes_proximity,
        "eyes_height": self.eyes_height,
        "eyes_size": self.eyes_size,
        "eyes_width": self.eyes_width,
        "eyes_length": self.eyes_length,
        "eyes_tilt": self.eyes_tilt,
        "eyes_closing": self.eyes_closing,
        
        "cheeks_proximity": self.cheeks_proximity,
        "cheeks_height": self.cheeks_height,
        "cheeks_size": self.cheeks_size,
        "cheeks_width": self.cheeks_width,
        "jaw_depth": self.jaw_depth,
        
        "nose_height": self.nose_height,
        "nose_width": self.nose_width,
        "nose_angle": self.nose_angle,
        
        "chin_size": self.chin_size,
        "chin_height": self.chin_height,
    }

    # Appliquer les shape keys pour tous les objets (head, eyes, et sourcils actifs)
    for key, value in shape_keys.items():
        if key in head.data.shape_keys.key_blocks:
            head.data.shape_keys.key_blocks[key].value = value
        if key in eyes.data.shape_keys.key_blocks:
            eyes.data.shape_keys.key_blocks[key].value = value
        if key in active_brows.data.shape_keys.key_blocks:
            active_brows.data.shape_keys.key_blocks[key].value = value

    print(f"Shape keys mises à jour pour head, eyes et {self.brows_type}")


def update_brows_shape_keys(self, context):
    """ Applique les shape keys uniquement sur les sourcils actifs """
    
    active_brows = bpy.data.objects.get(self.brows_type)

    if not active_brows or not active_brows.data.shape_keys:
        print(f"L'objet '{self.brows_type}' n'a pas de shape keys !")
        return

    shape_keys = {
    
        # Déjà synchronisées avec head/eyes
        "brows_height": self.brows_height,
        "brows_depth": self.brows_depth,
        
        # Shape keys spécifiques
        "brows_proximity": self.brows_proximity,
        "brows_size": self.brows_size,
        "brows_angle": self.brows_angle,
        "brows_thickness": self.brows_thickness,
        "brows_tilt": self.brows_tilt,
        
        "brows_arch": self.brows_arch,
        "brows_frown": self.brows_frown
    }

    for key, value in shape_keys.items():
        if key in active_brows.data.shape_keys.key_blocks:
            active_brows.data.shape_keys.key_blocks[key].value = value
        else:
            print(f"Shape Key '{key}' non trouvée sur '{self.brows_type}'.")
            
def update_brows(self, context):
    """ Active les sourcils sélectionnés et applique les shape keys uniquement à ceux-ci """
    
    # Définition des objets sourcils
    brows_objects = {
        "eyebrows1": bpy.data.objects.get("eyebrows1"),
        "eyebrows2": bpy.data.objects.get("eyebrows2"),
        "eyebrows3": bpy.data.objects.get("eyebrows3"),
    }

    # Désactiver tous les sourcils
    for brows in brows_objects.values():
        if brows:
            brows.hide_set(True)

    # Activer uniquement les sourcils sélectionnés
    active_brows = brows_objects.get(self.brows_type)
    if active_brows:
        active_brows.hide_set(False)
        print(f"Sourcils activés : {self.brows_type}")

    # Mettre à jour les shape keys des sourcils actifs
    update_brows_shape_keys(self, context)




def update_hair(self, context):
    """ Active la hairBase sélectionnée, met à jour le modificateur Boolean des bangs et applique un offset aux bangs """

    hair_objects = {
        "hb1": "hairBase1",
        "hb2": "hairBase2",
        "hb3": "hairBase3",
        "hb4": "hairBase4",
        "hb5": "hairBase5",
    }

    bangs_objects = {
        "boolBangs1": "boolBangs1",
        "boolBangs2": "boolBangs2",
        "boolBangs3": "boolBangs3",
        "boolBangs4": "boolBangs4",
    }

    # Définition des offsets en fonction de la hairBase sélectionnée
    bangs_offsets = {
        "hb1": (0.0, 0.0, 0.0),
        "hb2": (0.0, -0.1, -0.2),
        "hb3": (0.0, -0.3, -0.25),
        "hb4": (0.0, -0.1, -0.3),
        "hb5": (0.0, -0.2, -0.3),
    }

    selected_hair = hair_objects.get(self.hair_base, None)
    selected_bangs = bangs_objects.get(self.bangs, None)
    new_position = bangs_offsets.get(self.hair_base, (0.0, 0.0, 0.0))

    # Désactiver toutes les hairBase avant d'activer la sélectionnée
    for obj_name in hair_objects.values():
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.hide_set(True)  # Cache l'objet

    # Activer uniquement la hairBase sélectionnée
    if selected_hair:
        obj = bpy.data.objects.get(selected_hair)
        if obj:
            obj.hide_set(False)  # Affiche l'objet
            print(f"HairBase activée : {selected_hair}")

            # Mise à jour du modificateur Boolean pour les bangs sélectionnés
            bool_modifier = None
            for mod in obj.modifiers:
                if mod.type == 'BOOLEAN' and mod.name == "BooleanBangs":
                    bool_modifier = mod
                    break
            
            if bool_modifier:
                bool_modifier.show_viewport = True
                bool_modifier.object = bpy.data.objects.get(selected_bangs) if selected_bangs else None
                print(f"Modificateur Boolean mis à jour avec {selected_bangs}.")
    
    # Appliquer la position absolue SEULEMENT au bangs sélectionné
    if selected_bangs:
        bangs_obj = bpy.data.objects.get(selected_bangs)
        if bangs_obj:
            bangs_obj.location = new_position  # Affectation directe en world space
            print(f"Position absolue appliquée à {selected_bangs} : {new_position}")




class BUSTE_PT_CustomizerPanel(bpy.types.Panel):
    bl_label = "Character Maker 3D Portrait"
    bl_idname = "BUSTE_PT_CustomizerPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Character Maker"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.buste_customizer
        
        # Hair options
        box = layout.box()
        box.label(text="Hair Settings")
        box.prop(props, "hair_base", text="Base")
        box.prop(props, "bangs", text="Bangs")
        
        # Ears options
        box = layout.box()
        box.label(text="Ear Settings")
        box.prop(props, "ear_type", text="Type")
        box.prop(props, "earrings_R", text="Right Earrings")
        box.prop(props, "earrings_L", text="Left Earrings")
        
        # Eyes options
        box = layout.box()
        box.label(text="Eye Settings")
        box.prop(props, "eyelashes", text="Eyelashes")
        box.prop(props, "eye_shape", text="Shape")
        box.prop(props, "pupil_texture", text="Pupil Texture")

        # Eyebrows Shape Keys
        box = layout.box()
        box.label(text="Eyebrows Settings")
        box.prop(props, "brows_type", text="Eyebrows Type")
        shape_keys = [
            "brows_height",
            "brows_depth",
            
            "brows_proximity",
            "brows_size",
            "brows_angle",
            "brows_thickness",
            "brows_tilt",
            
            "brows_arch",
            "brows_frown"
        ]
        
        for key in shape_keys:
            box.prop(props, key)
        
        # Eyes Shape Keys
        box = layout.box()
        box.label(text="Eyes Settings")
        shape_keys = [
            "eyes_proximity",
            "eyes_height",
            "eyes_size",
            "eyes_width",
            "eyes_length",
            "eyes_tilt",
            "eyes_closing"
        ]
        
        for key in shape_keys:
            box.prop(props, key)
        
        # Cheeks Shape Keys
        box = layout.box()
        box.label(text="Cheeks Settings")
        shape_keys = [
            "cheeks_proximity",
            "cheeks_height",
            "cheeks_size",
            "cheeks_width",
            "jaw_depth"
        ]
        
        for key in shape_keys:
            box.prop(props, key)
        
        # Nose Shape Keys
        box = layout.box()
        box.label(text="Nose Settings")
        shape_keys = [
            "nose_height",
            "nose_width",
            "nose_angle"
        ]
        
        for key in shape_keys:
            box.prop(props, key)
        
        # Chin Shape Keys
        box = layout.box()
        box.label(text="Chin Settings")
        shape_keys = [
            "chin_size",
            "chin_height"
        ]
        
        for key in shape_keys:
            box.prop(props, key)
        
        # Mouth options
        box = layout.box()
        box.label(text="Mouth Settings")
        box.prop(props, "mouth_texture", text="Texture")

class BUSTE_CustomizerProperties(bpy.types.PropertyGroup):
    
    # Eyebrows
    brows_type: bpy.props.EnumProperty(
        name="Eyebrows Type",
        items=[
            ("eyebrows1", "Eyebrows 1", ""),
            ("eyebrows2", "Eyebrows 2", ""),
            ("eyebrows3", "Eyebrows 3", ""),
        ],
        default="eyebrows1",
        update=update_brows
    )


    brows_height: bpy.props.FloatProperty(
        name="Eyebrows Height", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    brows_depth: bpy.props.FloatProperty(
        name="Eyebrows Depth", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    brows_proximity: bpy.props.FloatProperty(
        name="Eyebrows Proximity", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys
    )

    brows_size: bpy.props.FloatProperty(
        name="Eyebrows Size", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys
    )

    brows_angle: bpy.props.FloatProperty(
        name="Eyebrows Angle", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys
    )

    brows_thickness: bpy.props.FloatProperty(
        name="Eyebrows Thickness", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys
    )

    brows_tilt: bpy.props.FloatProperty(
        name="Eyebrows Tilt", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys
    )

    brows_arch: bpy.props.FloatProperty(
        name="Eyebrows Arch", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys
    )

    brows_frown: bpy.props.FloatProperty(
        name="Eyebrows Frown", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys
    )



    # Eyes
    eyes_proximity: bpy.props.FloatProperty(
        name="Eyes Proximity", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    eyes_height: bpy.props.FloatProperty(
        name="Eyes Height", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    eyes_size: bpy.props.FloatProperty(
        name="Eyes Size", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    eyes_width: bpy.props.FloatProperty(
        name="Eyes Width", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    eyes_length: bpy.props.FloatProperty(
        name="Eyes Length", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    eyes_tilt: bpy.props.FloatProperty(
        name="Eyes Tilt", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    eyes_closing: bpy.props.FloatProperty(
        name="Eyes Closing", min=0.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )



    # Cheeks & Jaw
    cheeks_proximity: bpy.props.FloatProperty(
        name="Cheeks Proximity", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    cheeks_height: bpy.props.FloatProperty(
        name="Cheeks Height", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    cheeks_size: bpy.props.FloatProperty(
        name="Cheeks Size", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    cheeks_width: bpy.props.FloatProperty(
        name="Cheeks Width", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    jaw_depth: bpy.props.FloatProperty(
        name="Jaw Depth", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )



    # Nose
    nose_height: bpy.props.FloatProperty(
        name="Nose Height", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    nose_width: bpy.props.FloatProperty(
        name="Nose Width", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    nose_angle: bpy.props.FloatProperty(
        name="Nose Angle", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    # Chin
    chin_size: bpy.props.FloatProperty(
        name="Chin Size", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )

    chin_height: bpy.props.FloatProperty(
        name="Chin Height", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys
    )



    # Hair
    hair_base: bpy.props.EnumProperty(
        name="Base Hair",
        items=[
            ("hb1", "Classic", ""),
            ("hb2", "Round", ""),
            ("hb3", "Tressed", ""),
            ("hb4", "Arranged", ""),
            ("hb5", "Parted", ""),
            ("bald", "Bald", "")
        ],
        update=update_hair
    )

    bangs: bpy.props.EnumProperty(
        name="Bangs",
        items=[
            ("none", "None", ""),
            ("boolBangs1", "Shell", ""),
            ("boolBangs2", "Side", ""),
            ("boolBangs3", "Heart", ""),
            ("boolBangs4", "Asymmetrical Heart", "")
        ],
        update=update_hair
    )



    # Ears
    ear_type: bpy.props.EnumProperty(
        name="Ear Type",
        items=[
            ("human", "Human", ""),
            ("elfe", "Elfe", ""),
            ("fae", "Fae", "")
        ],
        update=update_ears
    )

    earrings_L: bpy.props.EnumProperty(
        name="Left Earrings",
        items=[
            ("stud", "Stud", ""),
            ("hoop", "Hoop", ""),
            ("drop", "Drop", "")
        ],
        update=update_ears
    )

    earrings_R: bpy.props.EnumProperty(
        name="Right Earrings",
        items=[
            ("stud", "Stud", ""),
            ("hoop", "Hoop", ""),
            ("drop", "Drop", "")
        ],
        update=update_ears
    )



    # Eyelashes
    eyelashes: bpy.props.BoolProperty(
        name="Eyelashes", default=True
    )

    pupil_texture: bpy.props.EnumProperty(
        name="Pupil Texture",
        items=[
            ("default", "Default", ""),
            ("cat", "Cat", ""),
            ("star", "Star", "")
        ]
    )

    # Mouth
    mouth_texture: bpy.props.EnumProperty(
        name="Mouth Texture",
        items=[
            ("default", "Default", ""),
            ("smile", "Smile", ""),
            ("serious", "Serious", "")
        ]
    )

classes = [BUSTE_PT_CustomizerPanel, BUSTE_CustomizerProperties]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.buste_customizer = bpy.props.PointerProperty(type=BUSTE_CustomizerProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.buste_customizer

if __name__ == "__main__":
    register()