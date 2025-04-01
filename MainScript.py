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

    # Shape keys associées
    shape_keys = {
        "brows_height": self.brows_height,
        "brows_depth": self.brows_depth,
        
        "eyes_height": self.eyes_height,
        "eyes_distance": self.eyes_distance,
        
        "corner_EXT": self.corner_EXT,
        "corner_INT": self.corner_INT,
        
        "eyelid_T_height": self.eyelid_T_height,
        "eyelid_T_angle": self.eyelid_T_angle,
        "eyelid_B_height": self.eyelid_B_height,
        "eyelid_B_angle": self.eyelid_B_angle }

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

def update_brows_shape_keys(self, context):
    active_brows = bpy.data.objects.get(self.brows_type)
    if not active_brows or not active_brows.data.shape_keys:
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
        "brows_frown": self.brows_frown}

    for key, value in shape_keys.items():
        if key in active_brows.data.shape_keys.key_blocks:
            active_brows.data.shape_keys.key_blocks[key].value = value
        else:
            print(f"Shape Key '{key}' non trouvée sur '{self.brows_type}'.")
            
def update_brows(self, context):
    brows_objects = {
        "eyebrows1": bpy.data.objects.get("eyebrows1"),
        "eyebrows2": bpy.data.objects.get("eyebrows2"),
        "eyebrows3": bpy.data.objects.get("eyebrows3"),}

    # Désactiver tous les sourcils
    for brows in brows_objects.values():
        if brows:
            brows.hide_set(True)

    # Activer uniquement les sourcils sélectionnés
    active_brows = brows_objects.get(self.brows_type)
    if active_brows:
        active_brows.hide_set(False)

    # Mettre à jour les shape keys des sourcils actifs
    update_brows_shape_keys(self, context)

def update_eyelashes(self, context):
    eyelashes_objects = {
        "eyelashes1": bpy.data.objects.get("eyelashes1"),
        "eyelashes2": bpy.data.objects.get("eyelashes2"),
        "eyelashes3": bpy.data.objects.get("eyelashes3"),}

    # Désactiver tous les cils
    for eyelashes in eyelashes_objects.values():
        if eyelashes:
            eyelashes.hide_set(True)

    # Activer uniquement les cils sélectionnés
    active_eyelashes = eyelashes_objects.get(self.eyelashes_type)
    if active_eyelashes:
        active_eyelashes.hide_set(False)
    
    # Mettre à jour les shape keys des cils actifs
    update_facial_shape_keys(self, context)

def update_pupils(self, context):
    pupils_textures = {
        "pupil1": bpy.data.images.get("pupilsText1.png"),
        "pupil2": bpy.data.images.get("pupilsText2.png"),
        "pupil3": bpy.data.images.get("pupilsText3.png"),}

    selected_texture = pupils_textures.get(self.pupils_textures)
    if not selected_texture:
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

def update_hair(self, context):
    hairstyle_objects = {
        "hairstyle1": "hairstyle1",
        "hairstyle2": "hairstyle2",
        "hairstyle3": "hairstyle3",}
    hair_objects = {
        "hb1": "hairBase1",
        "hb2": "hairBase2",
        "hb3": "hairBase3",
        "hb4": "hairBase4",
        "hb5": "hairBase5",}
    bangs_objects = {
        "boolBangs1": "boolBangs1",
        "boolBangs2": "boolBangs2",
        "boolBangs3": "boolBangs3",
        "boolBangs4": "boolBangs4",
        "boolBangs5": "boolBangs5",}
    strands_objects = {
        "boolStrands1": "boolStrands1",
        "boolStrands2": "boolStrands2",
        "boolStrands3": "boolStrands3",}
    back_objects = {
        "boolBack1": "boolBack1",
        "boolBack2": "boolBack2",
        "boolBack3": "boolBack3",
        "boolBack4": "boolBack4"}
    bangs_offsets = {
        "hb1": (0.0, 0.0, 0.0),
        "hb2": (0.0, -0.1, -0.2),
        "hb3": (0.0, -0.3, -0.25),
        "hb4": (0.0, -0.1, -0.3),
        "hb5": (0.0, -0.2, -0.3),}
    selected_hairstyle = hairstyle_objects.get(self.hairstyle, None)
    selected_hair = hair_objects.get(self.hair_base, None)
    selected_bangs = bangs_objects.get(self.bangs, None)
    selected_strands = strands_objects.get(self.strands, None)
    selected_back = back_objects.get(self.back, None)
    new_position = bangs_offsets.get(self.hair_base, (0.0, 0.0, 0.0))
    # Désactiver toutes les coiffures, dabord les bases puis les hairstyles :
    for obj_name in hair_objects.values():
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.hide_set(True)
    for obj_name in hairstyle_objects.values():
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.hide_set(True)
    # Arrêt de la méthode si une hairstyle est choisie + activation hairstyle sélectionnée :
    if selected_hairstyle and not self.show_detailed_hair:
        obj = bpy.data.objects.get(selected_hairstyle)
        if obj:
            obj.hide_set(False)
        return
    # Arrêt de la méthode si le personnage est chauve :
    if self.hair_base == "bald":
        return
    # Activation de la hairbase sélectionnée :
    if selected_hair:
        obj = bpy.data.objects.get(selected_hair)
        if obj:
            obj.hide_set(False)
            # Application des bangs sélectionnées au Boolean correspondant :
            bool_modifier_bangs = next((mod for mod in obj.modifiers if mod.type == 'BOOLEAN' and mod.name == "BooleanBangs"), None)
            if bool_modifier_bangs:
                bool_modifier_bangs.show_viewport = True
                bool_modifier_bangs.object = bpy.data.objects.get(selected_bangs) if selected_bangs else None
            # Application des strands sélectionnées au Boolean correspondant :
            bool_modifier_strands = next((mod for mod in obj.modifiers if mod.type == 'BOOLEAN' and mod.name == "BooleanStrands"), None)
            if bool_modifier_strands:
                bool_modifier_strands.show_viewport = True
                bool_modifier_strands.object = bpy.data.objects.get(selected_strands) if selected_strands else None
            # Application du back sélectionné au Boolean correspondant :
            bool_modifier_back = next((mod for mod in obj.modifiers if mod.type == 'BOOLEAN' and mod.name == "BooleanBack"), None)
            if bool_modifier_back:
                bool_modifier_back.show_viewport = True
                bool_modifier_back.object = bpy.data.objects.get(selected_back) if selected_back else None
    # Application de l'offset pour les bangs en world space :
    if selected_bangs:
        bangs_obj = bpy.data.objects.get(selected_bangs)
        if bangs_obj:
            bangs_obj.location = new_position

class BUSTE_OT_SetEarSection(bpy.types.Operator):
    bl_idname = "buste.set_ear_section"
    bl_label = "Set Ear Section"
    
    section: bpy.props.StringProperty()
    
    def execute(self, context):
        props = context.scene.buste_customizer
        props.open_ear_section = self.section

        # Mise à jour de l'image associée
        if self.section == "ear_type":
            props.ear_image = "ear_base"
        elif self.section == "earrings_L":
            props.ear_image = "ear_lobe_L"
        elif self.section == "earrings_R":
            props.ear_image = "ear_lobe_R"
        elif self.section == "helix_L":
            props.ear_image = "ear_helix_L"
        elif self.section == "helix_R":
            props.ear_image = "ear_helix_R"
        
        return {'FINISHED'}

class BUSTE_OT_SetEyeSection(bpy.types.Operator):
    bl_idname = "buste.set_eye_section"
    bl_label = "Set Eye Section"
    
    section: bpy.props.StringProperty()
    
    def execute(self, context):
        props = context.scene.buste_customizer
        props.open_eye_section = self.section

        # Mise à jour de l'image associée
        if self.section == "eyelashes_type":
            props.eye_image = "eyes_eyelashes"
        elif self.section == "pupils_textures":
            props.eye_image = "eyes_pupil"
        elif self.section == "corner_EXT":
            props.eye_image = "eyes_corner_EXT"
        elif self.section == "corner_INT":
            props.eye_image = "eyes_corner_INT"
        elif self.section == "eyelid_T":
            props.eye_image = "eyes_eyelid_T"
        elif self.section == "eyelid_B":
            props.eye_image = "eyes_eyelid_B"
        elif self.section == "eyes_distance":
            props.eye_image = "eyes_distance"
        elif self.section == "eyes_height":
            props.eye_image = "eyes_height"
        elif self.section == "":
            props.eye_image = ""
        elif self.section == "":
            props.eye_image = ""
        elif self.section == "":
            props.eye_image = ""
        
        return {'FINISHED'}

class BUSTE_OT_SetBrowSection(bpy.types.Operator):
    bl_idname = "buste.set_brow_section"
    bl_label = "Set Brow Section"

    section: bpy.props.StringProperty()

    def execute(self, context):
        props = context.scene.buste_customizer
        props.open_brow_section = self.section

        # Mise à jour de l'image associée
        if self.section == "brows_type":
            props.brow_image = "brows_type"
        elif self.section == "brows_height":
            props.brow_image = "brows_height"
        elif self.section == "brows_depth":
            props.brow_image = "brows_depth"
        elif self.section == "brows_proximity":
            props.brow_image = "brows_proximity"
        elif self.section == "brows_size":
            props.brow_image = "brows_size"
        elif self.section == "brows_angle":
            props.brow_image = "brows_angle"
        elif self.section == "brows_thickness":
            props.brow_image = "brows_thickness"
        elif self.section == "brows_tilt":
            props.brow_image = "brows_tilt"
        elif self.section == "brows_arch":
            props.brow_image = "brows_arch"
        elif self.section == "brows_frown":
            props.brow_image = "brows_frown"

        return {'FINISHED'}
    
class BUSTE_OT_SetHairSection(bpy.types.Operator):
    bl_idname = "buste.set_hair_section"
    bl_label = "Set Hair Section"
    
    section: bpy.props.StringProperty()
    
    def execute(self, context):
        props = context.scene.buste_customizer
        props.open_hair_section = self.section

        # Mise à jour de l'image associée
        if self.section == "hair_default":
            props.hair_image = "hair_default"
        elif self.section == "hair_base":
            props.hair_image = "hair_base"
        elif self.section == "bangs":
            props.hair_image = "hair_bangs"
        elif self.section == "strands":
            props.hair_image = "hair_strands"
        elif self.section == "back":
            props.hair_image = "hair_back"
        
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

        # EARS SETTINGS ____________________________________________________________________________________________
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text="——— Ears Settings ———")
        row = box.row()
        row.operator("buste.set_ear_section", text="Type").section = "ear_type"
        row = box.row()
        box.separator()
        if "main" in preview_collections and props.ear_image in preview_collections["main"]:
            row.template_icon(preview_collections["main"][props.ear_image].icon_id, scale=6.0)
        box.separator()
        split = box.split(factor=0.5)
        col_L = split.column()
        col_R = split.column()
        col_L.operator("buste.set_ear_section", text="Right Helix").section = "helix_R"
        col_R.operator("buste.set_ear_section", text="Left Helix").section = "helix_L"
        split = box.split(factor=0.5)
        col_L = split.column()
        col_R = split.column()
        col_L.operator("buste.set_ear_section", text="Right Lobe").section = "earrings_R"
        col_R.operator("buste.set_ear_section", text="Left Lobe").section = "earrings_L"
        box.separator()
        if props.open_ear_section == "ear_type":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Ears Type :")
            col_R = split.column()
            col_R.prop(props, "ear_type", text="")
        elif props.open_ear_section == "earrings_L":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Left Lobe Earrings :")
            col_R = split.column()
            col_R.prop(props, "earrings_L", text="")
        elif props.open_ear_section == "earrings_R":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Right Lobe Earrings :")
            col_R = split.column()
            col_R.prop(props, "earrings_R", text="")
        elif props.open_ear_section == "helix_L":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Left Helix Earrings :")
            col_R = split.column()
            col_R.prop(props, "helix_L", text="")
        elif props.open_ear_section == "helix_R":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Right Helix Earrings :")
            col_R = split.column()
            col_R.prop(props, "helix_R", text="")
        box.separator()
        
        layout.separator()
        layout.separator()

        # EYES SETTINGS ____________________________________________________________________________________________
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text="——— Eyes Settings ———")
        row = box.column()
        row.operator("buste.set_eye_section", text="Eyelashes").section = "eyelashes_type"
        row.operator("buste.set_eye_section", text="Pupils").section = "pupils_textures"
        box.separator()
        row = box.row()
        if "main" in preview_collections and props.eye_image in preview_collections["main"]:
            row.template_icon(preview_collections["main"][props.eye_image].icon_id, scale=6.0)
        box.separator()
        box.operator("buste.set_eye_section", text="Top Eyelid").section = "eyelid_T"
        split = box.split(factor=0.5)
        col_L = split.column()
        col_R = split.column()
        col_L.operator("buste.set_eye_section", text="Medial Canthus").section = "corner_INT"
        col_R.operator("buste.set_eye_section", text="Lateral Canthus").section = "corner_EXT"
        box.operator("buste.set_eye_section", text="Bottom Eyelid").section = "eyelid_B"
        box.separator()
        row = box.column()
        row.operator("buste.set_eye_section", text="Eyes Height").section = "eyes_height"
        row.operator("buste.set_eye_section", text="Eyes Distance").section = "eyes_distance"
        box.separator()
        if props.open_eye_section == "eyelashes_type":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyelashes Type :")
            col_R = split.column()
            col_R.prop(props, "eyelashes_type", text="")
        elif props.open_eye_section == "pupils_textures":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Pupils Shape :")
            col_R = split.column()
            col_R.prop(props, "pupils_textures", text="")
        elif props.open_eye_section == "corner_EXT":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Lateral Canthus :")
            col_R = split.column()
            col_R.prop(props, "corner_EXT", text="")
        elif props.open_eye_section == "corner_INT":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Medial Canthus :")
            col_R = split.column()
            col_R.prop(props, "corner_INT", text="")
        elif props.open_eye_section == "eyelid_T":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Top Eyelid :")
            col_R = split.column()
            col_R.prop(props, "eyelid_T_height", text="Height")
            col_R.prop(props, "eyelid_T_angle", text="Angle")
        elif props.open_eye_section == "eyelid_B":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Bottom Eyelid :")
            col_R = split.column()
            col_R.prop(props, "eyelid_B_height", text="Height")
            col_R.prop(props, "eyelid_B_angle", text="Angle")
        elif props.open_eye_section == "eyes_height":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyes height :")
            col_R = split.column()
            col_R.prop(props, "eyes_height", text="")
        elif props.open_eye_section == "eyes_distance":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyes Distance :")
            col_R = split.column()
            col_R.prop(props, "eyes_distance", text="")
        box.separator()
        
        layout.separator()
        layout.separator()
        
        # BROWS SETTINGS ____________________________________________________________________________________________
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text="——— Brows Settings ———")
        row = box.column()
        row.operator("buste.set_brow_section", text="Type").section = "brows_type"
        row.operator("buste.set_brow_section", text="Thickness").section = "brows_thickness"
        row = box.row()
        row.operator("buste.set_brow_section", text="Size").section = "brows_size"
        row.operator("buste.set_brow_section", text="Angle").section = "brows_angle"
        row = box.row()
        if "main" in preview_collections and props.brow_image in preview_collections["main"]:
            row.template_icon(preview_collections["main"][props.brow_image].icon_id, scale=6.0)
        row = box.row()
        row.operator("buste.set_brow_section", text="Frown").section = "brows_frown"
        row.operator("buste.set_brow_section", text="Arch").section = "brows_arch"
        row.operator("buste.set_brow_section", text="Tilt").section = "brows_tilt"
        row = box.column()
        row.operator("buste.set_brow_section", text="Height").section = "brows_height"
        row.operator("buste.set_brow_section", text="Proximity").section = "brows_proximity"
        row.operator("buste.set_brow_section", text="Depth").section = "brows_depth"
        box.separator()
        if props.open_brow_section == "brows_type":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Type :")
            col_R = split.column()
            col_R.prop(props, "brows_type", text="")
        elif props.open_brow_section == "brows_thickness":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Thickness :")
            col_R = split.column()
            col_R.prop(props, "brows_thickness", text="")
        elif props.open_brow_section == "brows_size":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Size :")
            col_R = split.column()
            col_R.prop(props, "brows_size", text="")
        elif props.open_brow_section == "brows_angle":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Angle :")
            col_R = split.column()
            col_R.prop(props, "brows_angle", text="")
        elif props.open_brow_section == "brows_frown":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Frown :")
            col_R = split.column()
            col_R.prop(props, "brows_frown", text="")
        elif props.open_brow_section == "brows_arch":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Arch :")
            col_R = split.column()
            col_R.prop(props, "brows_arch", text="")
        elif props.open_brow_section == "brows_tilt":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Tilt :")
            col_R = split.column()
            col_R.prop(props, "brows_tilt", text="")
        elif props.open_brow_section == "brows_height":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Height :")
            col_R = split.column()
            col_R.prop(props, "brows_height", text="")
        elif props.open_brow_section == "brows_proximity":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Proximity :")
            col_R = split.column()
            col_R.prop(props, "brows_proximity", text="")
        elif props.open_brow_section == "brows_depth":
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Eyebrows Depth :")
            col_R = split.column()
            col_R.prop(props, "brows_depth", text="")
        box.separator()
        
        layout.separator()
        layout.separator()

        # HAIR SETTINGS ____________________________________________________________________________________________
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text="——— Hair Settings ———")
        row = box.row()
        row.alignment = 'CENTER'
        row.prop(props, "show_detailed_hair", text="Detailed Hair Options")
        if props.show_detailed_hair:
            row = box.row()
            box.separator()
            if "main" in preview_collections and props.hair_image in preview_collections["main"]:
                row.template_icon(preview_collections["main"][props.hair_image].icon_id, scale=6.0)
            row = box.row()
            row.operator("buste.set_hair_section", text="Base").section = "hair_base"
            row = box.row()
            row.operator("buste.set_hair_section", text="Bangs").section = "bangs"
            row.operator("buste.set_hair_section", text="Strands").section = "strands"
            row.operator("buste.set_hair_section", text="Back").section = "back"
            box.separator()
            if props.open_hair_section == "hair_base":
                split = box.split(factor=0.5)
                col_L = split.column()
                col_L.label(text="Hair Base :")
                col_R = split.column()
                col_R.prop(props, "hair_base", text="")
            elif props.open_hair_section == "bangs":
                split = box.split(factor=0.5)
                col_L = split.column()
                col_L.label(text="Hair Bangs :")
                col_R = split.column()
                col_R.prop(props, "bangs", text="")
            elif props.open_hair_section == "strands":
                split = box.split(factor=0.5)
                col_L = split.column()
                col_L.label(text="Hair Strands :")
                col_R = split.column()
                col_R.prop(props, "strands", text="")
            elif props.open_hair_section == "back":
                split = box.split(factor=0.5)
                col_L = split.column()
                col_L.label(text="Back Hair :")
                col_R = split.column()
                col_R.prop(props, "back", text="")
        else:
            row = box.row()
            box.separator()
            if "main" in preview_collections and props.hair_image in preview_collections["main"]:
                row.template_icon(preview_collections["main"][props.hair_image].icon_id, scale=6.0)
            box.separator()
            split = box.split(factor=0.5)
            col_L = split.column()
            col_L.label(text="Hair Style :")
            col_R = split.column()
            col_R.prop(props, "hairstyle", text="")
        box.separator()
            
class BUSTE_CustomizerProperties(bpy.types.PropertyGroup):
    # EARS SETTINGS ____________________________________________________________________________________________
    open_ear_section: bpy.props.StringProperty(default="ear_type")
    ear_image: bpy.props.StringProperty(name="Ear Image", default="ear_default")
    ear_type: bpy.props.EnumProperty(name="Ear Type", items=[
            ("human", "Human", ""),
            ("elfe", "Elfe", ""),
            ("fae", "Fae", "")
        ], update=update_ears)
    earrings_L: bpy.props.EnumProperty(name="Left Lobe Earrings", items=[
            ("none", "None", ""),
            ("earrings_L1", "Stud", ""),
            ("earrings_L2", "Hoop", ""),
            ("earrings_L3", "Diamond Drop", ""),
            ("earrings_L4", "Ringued Drop", ""),
            ("earrings_L5", "Long Drop", "")
        ],update=update_ears)
    earrings_R: bpy.props.EnumProperty(name="Right Lobe Earrings", items=[
            ("none", "None", ""),
            ("earrings_R1", "Stud", ""),
            ("earrings_R2", "Hoop", ""),
            ("earrings_R3", "Diamond Drop", ""),
            ("earrings_R4", "Ringued Drop", ""),
            ("earrings_R5", "Long Drop", "")
        ], update=update_ears)
    helix_L: bpy.props.EnumProperty(name="Left Helix Earrings", items=[
            ("none", "None", ""),
            ("helix_L1", "Ring", ""),
            ("helix_L2", "Double Ring", ""),
            ("helix_L3", "Triple Ring", "")
        ], update=update_ears)
    helix_R: bpy.props.EnumProperty(name="Right Helix Earrings", items=[
            ("none", "None", ""),
            ("helix_R1", "Ring", ""),
            ("helix_R2", "Double Ring", ""),
            ("helix_R3", "Triple Ring", "")
        ], update=update_ears)
    
    # EYES SETTINGS ____________________________________________________________________________________________
    open_eye_section: bpy.props.StringProperty(default="eyelashes_type")
    eye_image: bpy.props.StringProperty(name="Eye Image", default="eyes_default")
    pupils_textures: bpy.props.EnumProperty(
        name="Pupils Shape",
        items=[
            ("pupil1", "Default", ""),
            ("pupil2", "Chocked", ""),
            ("pupil3", "Hypnotized", "")],
        update=update_pupils)
    eyelashes_type: bpy.props.EnumProperty(
        name="Eyelashes Type",
        items=[
            ("none", "None", ""),
            ("eyelashes1", "Simple", ""),
            ("eyelashes2", "Innocent", ""),
            ("eyelashes3", "Double Lashes", ""),],
        default="eyelashes1",
        update=update_eyelashes)
    eyes_height: bpy.props.FloatProperty(
        name="Eyes Height", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    eyes_distance: bpy.props.FloatProperty(
        name="Eyes Distance", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    corner_EXT: bpy.props.FloatProperty(
        name="Lateral Canthus", min=0.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    corner_INT: bpy.props.FloatProperty(
        name="Medial Canthus", min=0.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    eyelid_T_height: bpy.props.FloatProperty(
        name="Top Eyelid Height", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    eyelid_T_angle: bpy.props.FloatProperty(
        name="Top Eyelid Angle", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    eyelid_B_height: bpy.props.FloatProperty(
        name="Bottom Eyelid Height", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    eyelid_B_angle: bpy.props.FloatProperty(
        name="Bottom Eyelid Angle", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    
    # BROWS SETTINGS ____________________________________________________________________________________________
    open_brow_section: bpy.props.StringProperty(default="brows_type")
    brow_image: bpy.props.StringProperty(name="Brow Image", default="brows_default")
    brows_type: bpy.props.EnumProperty(
        name="Eyebrows Type",
        items=[
            ("eyebrows1", "Thin", ""),
            ("eyebrows2", "Large", ""),
            ("eyebrows3", "Round", ""),],
        default="eyebrows1",
        update=update_brows)
    brows_height: bpy.props.FloatProperty(
        name="Eyebrows Height", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    brows_depth: bpy.props.FloatProperty(
        name="Eyebrows Depth", min=-1.0, max=1.0, default=0.0,
        update=update_facial_shape_keys)
    brows_proximity: bpy.props.FloatProperty(
        name="Eyebrows Proximity", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys)
    brows_size: bpy.props.FloatProperty(
        name="Eyebrows Size", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys)
    brows_angle: bpy.props.FloatProperty(
        name="Eyebrows Angle", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys)
    brows_thickness: bpy.props.FloatProperty(
        name="Eyebrows Thickness", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys)
    brows_tilt: bpy.props.FloatProperty(
        name="Eyebrows Tilt", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys)
    brows_arch: bpy.props.FloatProperty(
        name="Eyebrows Arch", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys)
    brows_frown: bpy.props.FloatProperty(
        name="Eyebrows Frown", min=-1.0, max=1.0, default=0.0,
        update=update_brows_shape_keys)

    # HAIR SETTINGS ____________________________________________________________________________________________
    open_hair_section: bpy.props.StringProperty(default="hair_base")
    hair_image: bpy.props.StringProperty(name="Hair Image", default="hair_default")
    hair_base: bpy.props.EnumProperty(
        name="Base Hair",
        items=[
            ("hb1", "Classic", ""),
            ("hb2", "Round", ""),
            ("hb3", "Tressed", ""),
            ("hb4", "Arranged", ""),
            ("hb5", "Parted", ""),
            ("bald", "Bald", "")],
        update=update_hair)
    bangs: bpy.props.EnumProperty(
        name="Bangs",
        items=[
            ("none", "None", ""),
            ("boolBangs1", "Shell", ""),
            ("boolBangs2", "Side", ""),
            ("boolBangs3", "Symmetrical Heart", ""),
            ("boolBangs4", "Heart", ""),
            ("boolBangs5", "Pointy", "")],
        update=update_hair)
    strands: bpy.props.EnumProperty(
        name="Strands",
        items=[
            ("none", "None", ""),
            ("boolStrands1", "Long", ""),
            ("boolStrands2", "Soft", ""),
            ("boolStrands3", "Medusa", "")],
        update=update_hair)
    back: bpy.props.EnumProperty(
        name="Back",
        items=[
            ("none", "None", ""),
            ("boolBack1", "Long", ""),
            ("boolBack2", "Medium", ""),
            ("boolBack3", "Bun", ""),
            ("boolBack4", "Ponytail", "")],
        update=update_hair)
    hairstyle: bpy.props.EnumProperty(
        name="Hairstyle",
        items=[
            ("hairstyle1", "hairstyle 1", ""),
            ("hairstyle2", "hairstyle 2", ""),
            ("hairstyle3", "hairstyle 3", "")],
        update=update_hair)
    show_detailed_hair: bpy.props.BoolProperty(
        name="Detailed Hair Options",
        description="Toggle between detailed hair customization and preset selection",
        default=True,
    update=update_hair)

classes = [BUSTE_PT_CustomizerPanel, BUSTE_CustomizerProperties, BUSTE_OT_SetEarSection, BUSTE_OT_SetEyeSection, BUSTE_OT_SetBrowSection, BUSTE_OT_SetHairSection]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.buste_customizer = bpy.props.PointerProperty(type=BUSTE_CustomizerProperties)

    # Dossier sur PC ATI :
    ICON_DIR = r"D:\Git Repositories\Character-Maker-3D-Portrait\Icons"
    # Dossier sur PC perso :
    #ICON_DIR = r"D:\Documents\2024-2025\Python\S2\Character-Maker-3D-Portrait\Icons"
    
    # Dictionnaire des images à charger
    icon_files = {
        "ear_base": "ear_base.png",
        "ear_default": "ear_default.png",
        "ear_helix_L": "ear_helix_L.png",
        "ear_helix_R": "ear_helix_R.png",
        "ear_lobe_L": "ear_lobe_L.png",
        "ear_lobe_R": "ear_lobe_R.png",

        "eyes_corner_EXT": "eyes_corner_EXT.png",
        "eyes_corner_INT": "eyes_corner_INT.png",
        "eyes_default": "eyes_default.png",
        "eyes_distance": "eyes_distance.png",
        "eyes_eyelashes": "eyes_eyelashes.png",
        "eyes_eyelid_B": "eyes_eyelid_B.png",
        "eyes_eyelid_T": "eyes_eyelid_T.png",
        "eyes_height": "eyes_height.png",
        "eyes_pupil": "eyes_pupil.png",
        
        "brows_angle": "brows_angle.png",
        "brows_arch": "brows_arch.png",
        "brows_default": "brows_default.png",
        "brows_depth": "brows_depth.png",
        "brows_frown": "brows_frown.png",
        "brows_height": "brows_height.png",
        "brows_proximity": "brows_proximity.png",
        "brows_size": "brows_size.png",
        "brows_thickness": "brows_thickness.png",
        "brows_tilt": "brows_tilt.png",
        "brows_type": "brows_type.png",
        
        "hair_default": "hair_default.png",
        "hair_base": "hair_base.png",
        "hair_bangs": "hair_bangs.png",
        "hair_strands": "hair_strands.png",
        "hair_back": "hair_back.png"}

    # Charger les images dynamiquement
    icon_ids = {}
    for name, filename in icon_files.items():
        icon_path = os.path.join(ICON_DIR, filename)
        icon_ids[name] = load_image(name, icon_path) or 0  # Assure que la valeur par défaut est 0

    # Oreilles ID
    bpy.types.Scene.ear_preview_icon_1 = bpy.props.IntProperty(default=icon_ids["ear_default"])
    bpy.types.Scene.ear_preview_icon_2 = bpy.props.IntProperty(default=icon_ids["ear_base"])
    bpy.types.Scene.ear_preview_icon_3 = bpy.props.IntProperty(default=icon_ids["ear_lobe_L"])
    bpy.types.Scene.ear_preview_icon_4 = bpy.props.IntProperty(default=icon_ids["ear_lobe_R"])
    bpy.types.Scene.ear_preview_icon_5 = bpy.props.IntProperty(default=icon_ids["ear_helix_L"])
    bpy.types.Scene.ear_preview_icon_6 = bpy.props.IntProperty(default=icon_ids["ear_helix_R"])
    # Yeux ID
    bpy.types.Scene.eye_preview_icon_1 = bpy.props.IntProperty(default=icon_ids["eyes_default"])
    bpy.types.Scene.eye_preview_icon_2 = bpy.props.IntProperty(default=icon_ids["eyes_height"])
    bpy.types.Scene.eye_preview_icon_3 = bpy.props.IntProperty(default=icon_ids["eyes_corner_EXT"])
    bpy.types.Scene.eye_preview_icon_4 = bpy.props.IntProperty(default=icon_ids["eyes_corner_INT"])
    bpy.types.Scene.eye_preview_icon_5 = bpy.props.IntProperty(default=icon_ids["eyes_eyelid_T"])
    bpy.types.Scene.eye_preview_icon_6 = bpy.props.IntProperty(default=icon_ids["eyes_eyelid_B"])
    bpy.types.Scene.eye_preview_icon_7 = bpy.props.IntProperty(default=icon_ids["eyes_pupil"])
    bpy.types.Scene.eye_preview_icon_8 = bpy.props.IntProperty(default=icon_ids["eyes_eyelashes"])
    # Sourcils ID
    bpy.types.Scene.brows_preview_icon_1 = bpy.props.IntProperty(default=icon_ids["brows_default"])
    bpy.types.Scene.brows_preview_icon_2 = bpy.props.IntProperty(default=icon_ids["brows_angle"])
    bpy.types.Scene.brows_preview_icon_3 = bpy.props.IntProperty(default=icon_ids["brows_arch"])
    bpy.types.Scene.brows_preview_icon_4 = bpy.props.IntProperty(default=icon_ids["brows_depth"])
    bpy.types.Scene.brows_preview_icon_5 = bpy.props.IntProperty(default=icon_ids["brows_frown"])
    bpy.types.Scene.brows_preview_icon_6 = bpy.props.IntProperty(default=icon_ids["brows_height"])
    bpy.types.Scene.brows_preview_icon_7 = bpy.props.IntProperty(default=icon_ids["brows_proximity"])
    bpy.types.Scene.brows_preview_icon_8 = bpy.props.IntProperty(default=icon_ids["brows_size"])
    bpy.types.Scene.brows_preview_icon_9 = bpy.props.IntProperty(default=icon_ids["brows_thickness"])
    bpy.types.Scene.brows_preview_icon_10 = bpy.props.IntProperty(default=icon_ids["brows_tilt"])
    bpy.types.Scene.brows_preview_icon_10 = bpy.props.IntProperty(default=icon_ids["brows_type"])
    # Hair ID
    bpy.types.Scene.hair_preview_icon_1 = bpy.props.IntProperty(default=icon_ids["hair_default"])
    bpy.types.Scene.hair_preview_icon_2 = bpy.props.IntProperty(default=icon_ids["hair_base"])
    bpy.types.Scene.hair_preview_icon_3 = bpy.props.IntProperty(default=icon_ids["hair_bangs"])
    bpy.types.Scene.hair_preview_icon_4 = bpy.props.IntProperty(default=icon_ids["hair_strands"])
    bpy.types.Scene.hair_preview_icon_5 = bpy.props.IntProperty(default=icon_ids["hair_back"])

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Nettoyage des previews
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)

if __name__ == "__main__":
    register()
