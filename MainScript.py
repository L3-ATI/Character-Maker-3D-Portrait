import bpy
import bpy.utils.previews
import os

# Dictionnaire pour stocker les previews
preview_collections = {}

def load_image(image_name, image_path):
    """Charge une image personnalisée et la stocke dans la collection de previews"""
    if not os.path.exists(image_path):
        print(f"Erreur : L'image {image_path} est introuvable.")
        return None

    if "main" not in preview_collections:
        preview_collections["main"] = bpy.utils.previews.new()

    pcoll = preview_collections["main"]
    img_preview = pcoll.load(image_name, image_path, 'IMAGE')  
    return img_preview.icon_id

def update_ears(self, context):
    """Met à jour l'oreille et ajuste les boucles d'oreilles en fonction des choix sélectionnés."""
    
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

    # --- Mise à jour des boucles d'oreilles (Lobe + Hélix) ---
    
    # Boucles d'oreilles du lobe
    lobe_earring_objects = {
        "earrings1": ("earrings_L1", "earrings_R1"),
        "earrings2": ("earrings_L2", "earrings_R2"),
        "earrings3": ("earrings_L3", "earrings_R3"),
        "earrings4": ("earrings_L4", "earrings_R4"),
        "earrings5": ("earrings_L5", "earrings_R5")
    }

    # Boucles d'oreilles de l'hélix
    helix_earring_objects = {
        "helix1": ("helix_L1", "helix_R1"),
        "helix2": ("helix_L2", "helix_R2"),
        "helix3": ("helix_L3", "helix_R3")
    }

    # Offsets pour chaque type d'oreille
    lobe_offsets = {
        "human": (0.0, 0.0, 0.0),
        "elfe": (0.01, -0.01, 0.0),
        "fae": (0.05, -0.02, 0.0)
    }

    helix_offsets = {
        "human": (0.0, 0.0, 0.0),
        "elfe": (-0.05, -0.58, 1.7),
        "fae": (0.35, -0.63, 1.9)
    }
    
    # Offsets de rotation en radians
    from math import radians
    lobe_rotation_offsets = {
        "human": (radians(0), radians(0), radians(0)),
        "elfe": (radians(0), radians(0), radians(0)),
        "fae": (radians(0), radians(0), radians(0))
    }

    helix_rotation_offsets = {
        "human": (radians(0), radians(0), radians(0)),
        "elfe": (radians(-43), radians(33), radians(0)),
        "fae": (radians(-50), radians(40), radians(0))
    }

     # Récupérer les offsets selon le type d'oreille
    lobe_offset = lobe_offsets.get(self.ear_type, (0, 0, 0))
    helix_offset = helix_offsets.get(self.ear_type, (0, 0, 0))

    lobe_rotation_offset = lobe_rotation_offsets.get(self.ear_type, (0, 0, 0))
    helix_rotation_offset = helix_rotation_offsets.get(self.ear_type, (0, 0, 0))

    # Récupérer les boucles d'oreilles sélectionnées
    selected_lobe_L = self.earrings_L
    selected_lobe_R = self.earrings_R
    selected_helix_L = self.helix_L
    selected_helix_R = self.helix_R

    # Cacher toutes les boucles d'oreilles
    for earring_name in lobe_earring_objects.values():
        for obj_name in earring_name:
            obj = bpy.data.objects.get(obj_name)
            if obj:
                obj.hide_set(True)

    for earring_name in helix_earring_objects.values():
        for obj_name in earring_name:
            obj = bpy.data.objects.get(obj_name)
            if obj:
                obj.hide_set(True)

    # --- Activer et placer les boucles du lobe ---
    if selected_lobe_L:
        earring_obj_L = bpy.data.objects.get(selected_lobe_L)
        if earring_obj_L:
            earring_obj_L.hide_set(False)
            earring_obj_L.location = lobe_offset  # Coordonnées MONDE

    if selected_lobe_R:
        earring_obj_R = bpy.data.objects.get(selected_lobe_R)
        if earring_obj_R:
            earring_obj_R.hide_set(False)
            earring_obj_R.location = (-lobe_offset[0], lobe_offset[1], lobe_offset[2])  # Inversion en X

    # --- Activer et placer les boucles de l'hélix ---
    if selected_helix_L:
        helix_obj_L = bpy.data.objects.get(selected_helix_L)
        if helix_obj_L:
            helix_obj_L.hide_set(False)
            helix_obj_L.location = helix_offset  # Coordonnées MONDE
            helix_obj_L.rotation_euler = helix_rotation_offset  # Rotation MONDE

    if selected_helix_R:
        helix_obj_R = bpy.data.objects.get(selected_helix_R)
        if helix_obj_R:
            helix_obj_R.hide_set(False)
            helix_obj_R.location = (-helix_offset[0], helix_offset[1], helix_offset[2])  # Inversion en X
            helix_obj_R.rotation_euler = (helix_rotation_offset[0], -helix_rotation_offset[1], -helix_rotation_offset[2])  # Inversion en X et Z

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
    
    # Sélectionner les cils actifs
    eyelashes_objects = {
        "eyelashes1": bpy.data.objects.get("eyelashes1"),
        "eyelashes2": bpy.data.objects.get("eyelashes2"),
        "eyelashes3": bpy.data.objects.get("eyelashes3"),
    }
    
    active_eyelashes = eyelashes_objects.get(self.eyelashes_type)
        
    if not head or not head.data.shape_keys:
        print("L'objet 'head' n'a pas de shape keys !")
        return

    if not eyes or not eyes.data.shape_keys:
        print("L'objet 'eyes' n'a pas de shape keys !")
        return
    
    if not active_brows or not active_brows.data.shape_keys:
        print("L'objet 'eyebrows' n'a pas de shape keys !")
        return
    
    if not active_eyelashes or not active_eyelashes.data.shape_keys:
        print("L'objet 'eyelashes' sélectionné n'a pas de shape keys !")
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
        if key in active_eyelashes.data.shape_keys.key_blocks:
            active_eyelashes.data.shape_keys.key_blocks[key].value = value

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

def update_eyelashes(self, context):
    """ Active les sourcils sélectionnés et applique les shape keys uniquement à ceux-ci """
    
    # Définition des objets sourcils
    eyelashes_objects = {
        "eyelashes1": bpy.data.objects.get("eyelashes1"),
        "eyelashes2": bpy.data.objects.get("eyelashes2"),
        "eyelashes3": bpy.data.objects.get("eyelashes3"),
    }

    # Désactiver tous les sourcils
    for eyelashes in eyelashes_objects.values():
        if eyelashes:
            eyelashes.hide_set(True)

    # Activer uniquement les sourcils sélectionnés
    active_eyelashes = eyelashes_objects.get(self.eyelashes_type)
    if active_eyelashes:
        active_eyelashes.hide_set(False)
        print(f"Cils activés : {self.eyelashes_type}")
    
    # Mettre à jour les shape keys des cils actifs
    update_facial_shape_keys(self, context)

def update_pupils(self, context):
    print(f"update_pupils() appelé avec {self.pupils_textures}")
    """ Change la texture appliquée aux pupilles sans modifier leur géométrie """
    
    # Liste des textures attendues
    expected_textures = ["pupilsText1.png", "pupilsText2.png", "pupilsText3.png"]

    # Vérifier si toutes les textures sont chargées dans Blender
    missing_textures = [tex for tex in expected_textures if tex not in bpy.data.images]

    if missing_textures:
        print(f"⚠ Attention : Les textures suivantes ne sont pas chargées dans Blender : {missing_textures}")
    else:
        print("✅ Toutes les textures de pupilles sont bien chargées.")

    
    # Liste des textures disponibles
    pupils_textures = {
        "pupil1": bpy.data.images.get("pupilsText1.png"),
        "pupil2": bpy.data.images.get("pupilsText2.png"),
        "pupil3": bpy.data.images.get("pupilsText3.png"),
    }

    # Vérifier si la texture sélectionnée existe
    selected_texture = pupils_textures.get(self.pupils_textures)

    if not selected_texture:
        print(f"Erreur : la texture {self.pupils_textures} n'existe pas dans bpy.data.images")
        return  # Empêche l'application d'une texture inexistante


    if selected_texture:
        # Appliquer la texture aux deux pupilles
        for pupil_name in ["pupil_R", "pupil_L"]:
            pupil = bpy.data.objects.get(pupil_name)
            if pupil and pupil.active_material:
                mat = pupil.active_material
                nodes = mat.node_tree.nodes

                texture_node = None
                for node in nodes:
                    if node.type == "TEX_IMAGE":
                        texture_node = node
                        break  # On sort dès qu'on a trouvé le bon nœud
                
                if texture_node:  # Si un nœud a été trouvé
                    texture_node.image = selected_texture
                    texture_node.image.reload()  # Rafraîchir l'affichage

                else:
                    print(f"Attention : Aucun nœud Image Texture trouvé dans {pupil_name}")


        print(f"Pupilles activées : {self.pupils_textures}")

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

class BUSTE_OT_SetEarSection(bpy.types.Operator):
    bl_idname = "buste.set_ear_section"
    bl_label = "Set Ear Section"
    
    section: bpy.props.StringProperty()
    
    def execute(self, context):
        props = context.scene.buste_customizer
        props.open_ear_section = self.section

        # Mise à jour de l'image associée
        if self.section == "ear_type":
            props.ear_image = "icon_ear_base"
        elif self.section == "earrings_L":
            props.ear_image = "icon_ear_lobe_L"
        elif self.section == "earrings_R":
            props.ear_image = "icon_ear_lobe_R"
        elif self.section == "helix_L":
            props.ear_image = "icon_ear_helix_L"
        elif self.section == "helix_R":
            props.ear_image = "icon_ear_helix_R"
            
        elif self.section == "helix_both":
            props.ear_image = "icon_ear_default"  # Utiliser une image générique
            props.open_ear_section = "helix_both"

        elif self.section == "lobe_both":
            props.ear_image = "icon_ear_default"
            props.open_ear_section = "lobe_both"

        
        return {'FINISHED'}
    
class BUSTE_OT_ToggleSymmetry(bpy.types.Operator):
    """Active ou désactive la symétrie"""
    bl_idname = "buste.toggle_symmetry"
    bl_label = "Toggle Symmetry"

    target: bpy.props.StringProperty()

    def execute(self, context):
        props = context.scene.buste_customizer

        if self.target == "helix":
            props.helix_both = not props.helix_both
        elif self.target == "lobe":
            props.lobe_both = not props.lobe_both

        return {'FINISHED'}

class BUSTE_PT_CustomizerPanel(bpy.types.Panel):
    bl_label = "Character Maker 3D Portrait"
    bl_idname = "BUSTE_PT_CustomizerPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Character Maker"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.buste_customizer

        # Section Ears
        box = layout.box()
        box.label(text="——— Ears Settings ———")

        # Afficher l'image des oreilles
        row = box.row()
        if "main" in preview_collections and props.ear_image in preview_collections["main"]:
            row.template_icon(preview_collections["main"][props.ear_image].icon_id, scale=7.0)



        # Ajouter les boutons pour sélectionner la section
        row = box.row()
        row.operator("buste.set_ear_section", text="Ears Type").section = "ear_type"



        row = box.row()
        split = row.split(factor=0.3)  # 20% d’espace à gauche
        split.label(text="")  # Espace vide
        split = split.split(factor=0.6)  # 60% pour le bouton
        split.operator("buste.toggle_symmetry", text="Helix Earrings").target = "helix"
        row = box.row()
        split = row.split(factor=0.3)  # 20% d’espace à gauche
        split.label(text="")  # Espace vide
        split = split.split(factor=0.6)  # 60% pour le bouton
        split.operator("buste.toggle_symmetry", text="Lobe Earrings").target = "lobe"



       # Afficher les boutons selon la symétrie activée ou non
        if props.helix_both:
            box.operator("buste.set_ear_section", text="Helix (Both)").section = "helix_both"
        else:
            split = box.split(factor=0.5)
            col_L = split.column()
            col_R = split.column()
            col_L.operator("buste.set_ear_section", text="Right Helix").section = "helix_R"
            col_R.operator("buste.set_ear_section", text="Left Helix").section = "helix_L"

        if props.lobe_both:
            box.operator("buste.set_ear_section", text="Lobe (Both)").section = "lobe_both"
        else:
            split = box.split(factor=0.5)
            col_L = split.column()
            col_R = split.column()
            col_L.operator("buste.set_ear_section", text="Right Lobe").section = "earrings_R"
            col_R.operator("buste.set_ear_section", text="Left Lobe").section = "earrings_L"



        # Afficher la propriété sélectionnée
        if props.open_ear_section == "ear_type":
            box.prop(props, "ear_type")
        elif props.open_ear_section == "earrings_L":
            box.prop(props, "earrings_L")
        elif props.open_ear_section == "earrings_R":
            box.prop(props, "earrings_R")
        elif props.open_ear_section == "helix_L":
            box.prop(props, "helix_L")
        elif props.open_ear_section == "helix_R":
            box.prop(props, "helix_R")
        elif props.open_ear_section == "helix_both":
            box.prop(props, "helix_both")  # Afficher la propriété symétrique
        elif props.open_ear_section == "lobe_both":
            box.prop(props, "lobe_both")  # Afficher la propriété symétrique




class BUSTE_CustomizerProperties(bpy.types.PropertyGroup):
    # EAR SETTINGS
    open_ear_section: bpy.props.StringProperty(default="ear_type")
    ear_image: bpy.props.StringProperty(default="icon_ear_default")  # Image par défaut

    ear_type: bpy.props.EnumProperty(name="Ear Type", items=[("small", "Small", ""), ("large", "Large", "")])
    earrings_L: bpy.props.EnumProperty(name="Left Lobe", items=[("none", "None", ""), ("stud", "Stud", "")])
    earrings_R: bpy.props.EnumProperty(name="Right Lobe", items=[("none", "None", ""), ("hoop", "Hoop", "")])
    helix_L: bpy.props.EnumProperty(name="Left Helix", items=[("none", "None", ""), ("bar", "Bar", "")])
    helix_R: bpy.props.EnumProperty(name="Right Helix", items=[("none", "None", ""), ("ring", "Ring", "")])

    # Nouvelles propriétés pour stocker les valeurs des deux côtés en mode symétrique
    helix_both: bpy.props.EnumProperty(name="Helix Both", items=[("none", "None", ""), ("bar", "Bar", ""), ("ring", "Ring", "")])
    lobe_both: bpy.props.EnumProperty(name="Lobe Both", items=[("none", "None", ""), ("stud", "Stud", ""), ("hoop", "Hoop", "")])

    def update_ear_symmetry(self, context):
        if self.symetrize_helix:
            self.helix_L = self.helix_both
            self.helix_R = self.helix_both
        if self.symetrize_lobe:
            self.earrings_L = self.lobe_both
            self.earrings_R = self.lobe_both

    ear_type: bpy.props.EnumProperty(
        name="Ear Type",
        items=[
            ("human", "Human", ""),
            ("elfe", "Elfe", ""),
            ("fae", "Fae", "")
        ],
        update=update_ears
    )
    
    helix_both: bpy.props.EnumProperty(
        name="Helix Both",
        items=[("none", "None", ""), ("bar", "Bar", ""), ("ring", "Ring", "")],
        update=update_ear_symmetry
    )

    lobe_both: bpy.props.EnumProperty(
        name="Lobe Both",
        items=[("none", "None", ""), ("stud", "Stud", ""), ("hoop", "Hoop", "")],
        update=update_ear_symmetry
    )
    

    
    
    
    
    
    
    
    
    
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
    pupils_textures: bpy.props.EnumProperty(
        name="Pupils Shape",
        items=[
            ("pupil1", "Default", ""),
            ("pupil2", "Chocked", ""),
            ("pupil3", "Hypnotized", "")
        ],
        update=update_pupils
    )

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


    # Boucles d'oreilles du lobe
    earrings_L: bpy.props.EnumProperty(
        name="Left Lobe Earrings",
        items=[
            ("none", "None", ""),
            ("earrings_L1", "Stud", ""),
            ("earrings_L2", "Hoop", ""),
            ("earrings_L3", "Diamond Drop", ""),
            ("earrings_L4", "Ringued Drop", ""),
            ("earrings_L5", "Long Drop", "")
        ],
        update=update_ears
    )

    earrings_R: bpy.props.EnumProperty(
        name="Right Lobe Earrings",
        items=[
            ("none", "None", ""),
            ("earrings_R1", "Stud", ""),
            ("earrings_R2", "Hoop", ""),
            ("earrings_R3", "Diamond Drop", ""),
            ("earrings_R4", "Ringued Drop", ""),
            ("earrings_R5", "Long Drop", "")
        ],
        update=update_ears
    )

    # Boucles d'oreilles de l'hélix
    helix_L: bpy.props.EnumProperty(
        name="Left Helix Earrings",
        items=[
            ("none", "None", ""),
            ("helix_L1", "Ring", ""),
            ("helix_L2", "Double Ring", ""),
            ("helix_L3", "Triple Ring", "")
        ],
        update=update_ears
    )

    helix_R: bpy.props.EnumProperty(
        name="Right Helix Earrings",
        items=[
            ("none", "None", ""),
            ("helix_R1", "Ring", ""),
            ("helix_R2", "Double Ring", ""),
            ("helix_R3", "Triple Ring", "")
        ],
        update=update_ears
    )
    
    # Eyelashes
    eyelashes_type: bpy.props.EnumProperty(
        name="Eyelashes Type",
        items=[
            ("none", "None", ""),
            ("eyelashes1", "Simple", ""),
            ("eyelashes2", "Innocent", ""),
            ("eyelashes3", "Double Lashes", ""),
        ],
        default="eyelashes1",
        update=update_eyelashes
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

classes = [BUSTE_PT_CustomizerPanel, BUSTE_CustomizerProperties, BUSTE_OT_SetEarSection, BUSTE_OT_ToggleSymmetry]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.buste_customizer = bpy.props.PointerProperty(type=BUSTE_CustomizerProperties)

    # Définir le dossier contenant les icônes (modifiable facilement)
    ICON_DIR = r"D:\Git Repositories\Character-Maker-3D-Portrait\Icons"

    # Dictionnaire des images à charger
    icon_files = {
        "icon_ear_default": "icon_ear_default.png",
        "icon_ear_base": "icon_ear_base.png",
        "icon_ear_lobe_L": "icon_ear_lobe_L.png",
        "icon_ear_lobe_R": "icon_ear_lobe_R.png",
        "icon_ear_helix_L": "icon_ear_helix_L.png",
        "icon_ear_helix_R": "icon_ear_helix_R.png",
    }

    # Charger les images dynamiquement
    icon_ids = {}
    for name, filename in icon_files.items():
        icon_path = os.path.join(ICON_DIR, filename)
        icon_ids[name] = load_image(name, icon_path) or 0  # Assure que la valeur par défaut est 0

    # Stocker les ID d'icônes dans bpy.types.Scene
    bpy.types.Scene.ear_preview_icon_1 = bpy.props.IntProperty(default=icon_ids["icon_ear_default"])
    bpy.types.Scene.ear_preview_icon_2 = bpy.props.IntProperty(default=icon_ids["icon_ear_base"])
    bpy.types.Scene.ear_preview_icon_3 = bpy.props.IntProperty(default=icon_ids["icon_ear_lobe_L"])
    bpy.types.Scene.ear_preview_icon_4 = bpy.props.IntProperty(default=icon_ids["icon_ear_lobe_R"])
    bpy.types.Scene.ear_preview_icon_5 = bpy.props.IntProperty(default=icon_ids["icon_ear_helix_L"])
    bpy.types.Scene.ear_preview_icon_6 = bpy.props.IntProperty(default=icon_ids["icon_ear_helix_R"])


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Nettoyage des previews
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)

if __name__ == "__main__":
    register()