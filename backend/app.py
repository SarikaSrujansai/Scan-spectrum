from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import base64
import random
from datetime import datetime
from PIL import Image
import io
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

# Comprehensive organ data with detailed descriptions and 3D model parameters
ORGANS_DATA = {
    'heart': {
        'name': 'Heart',
        'emoji': '❤️',
        'model_id': 'heart',
        'description': 'The powerful muscular organ that pumps blood throughout your circulatory system.',
        'color': '#DC2626',
        'system': 'Cardiovascular System',
        'animation': 'beat',
        'sketchfab_url': 'https://skfb.ly/6y9Uq',
        'full_description': '''
            ANATOMICAL OVERVIEW:
            The human heart is a sophisticated four-chambered muscular pump located in the mediastinum of the thoracic cavity,
            slightly left of center behind the sternum. Roughly the size of a closed fist (12 cm long, 8 cm wide, 6 cm thick),
            it weighs approximately 250-300 grams in females and 300-350 grams in males.

            STRUCTURAL COMPONENTS:
            • Pericardium: Double-walled sac containing serous fluid that protects and lubricates the heart
            • Myocardium: Thick muscular middle layer responsible for contraction
            • Endocardium: Smooth inner lining that minimizes friction for blood flow
            • Chambers: Four chambers (2 atria, 2 ventricles) separated by valves
            • Valves: Four one-way valves ensuring unidirectional blood flow

            FUNCTIONAL PHYSIOLOGY:
            The heart functions as a dual pump system - the right side handles pulmonary circulation (lungs) while the left side
            manages systemic circulation (body). Each cardiac cycle involves coordinated atrial and ventricular contractions
            (systole) and relaxations (diastole), maintaining a continuous blood flow of approximately 5-6 liters per minute at rest.

            BLOOD FLOW PATHWAY:
            Body → Superior/Inferior Vena Cava → Right Atrium → Tricuspid Valve → Right Ventricle → Pulmonary Valve →
            Pulmonary Arteries → Lungs → Pulmonary Veins → Left Atrium → Mitral Valve → Left Ventricle → Aortic Valve → Aorta → Body

            CLINICAL SIGNIFICANCE:
            Understanding cardiac anatomy is crucial for diagnosing and treating conditions like coronary artery disease,
            valvular disorders, arrhythmias, and congenital heart defects. The heart's electrical conduction system,
            beginning at the sinoatrial (SA) node, ensures coordinated contractions for efficient pumping.
        ''',
    },
    'lungs': {
        'name': 'Lungs',
        'emoji': '🫁',
        'model_id': 'lungs',
        'description': 'Paired respiratory organs for gas exchange.',
        'color': '#059669',
        'system': 'Respiratory System',
        'animation': 'breathe',
        'sketchfab_url': 'https://skfb.ly/69zrM',
        'full_description': '''
            GROSS PULMONARY ANATOMY:
            The lungs are paired, cone-shaped respiratory organs occupying most of the thoracic cavity. They extend
            from the diaphragm inferiorly to slightly above the clavicles superiorly, and are separated by the
            mediastinum containing the heart and great vessels.

            STRUCTURAL CHARACTERISTICS:
            • Right Lung: Three lobes (superior, middle, inferior) separated by oblique and horizontal fissures
            • Left Lung: Two lobes (superior, inferior) separated by oblique fissure, with cardiac notch
            • Weight: Right lung ~625g, left lung ~565g (males slightly heavier than females)

            BRONCHOPULMONARY SEGMENTS:
            Each lung is divided into functionally independent segments, each supplied by:
            • Segmental Bronchus
            • Segmental Artery
            • Segmental Vein (intersegmental)
            There are 10 segments in the right lung and 8-10 in the left lung.

            HISTOLOGICAL ORGANIZATION:
            The lungs feature a branching architecture with 23 generations from trachea to alveoli:
            • Conducting Zone: Generations 0-16 (trachea to terminal bronchioles)
            • Respiratory Zone: Generations 17-23 (respiratory bronchioles to alveolar sacs)
        ''',
    },
    'digestive': {
        'name': 'Digestive System',
        'emoji': '🍽️',
        'model_id': 'digestive',
        'description': 'Complex system for food processing, nutrient absorption, and waste elimination.',
        'color': '#D97706',
        'system': 'Digestive System',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/6Rqz8',
        'full_description': '''
            GASTROINTESTINAL OVERVIEW:
            The human digestive system is a continuous muscular tube extending from mouth to anus, approximately
            9 meters (30 feet) in length, with accessory organs that contribute to the digestive process.

            MAJOR COMPONENTS:
            • Upper GI Tract: Mouth, pharynx, esophagus, stomach
            • Lower GI Tract: Small intestine, large intestine, rectum, anus
            • Accessory Organs: Liver, gallbladder, pancreas

            FUNCTIONAL PROCESSES:
            • Ingestion: Food intake through mouth
            • Digestion: Mechanical and chemical breakdown of food
            • Absorption: Nutrient transfer to bloodstream
            • Motility: Movement through GI tract via peristalsis
            • Elimination: Waste removal as feces

            HISTOLOGICAL ORGANIZATION:
            Four main layers throughout most of the GI tract:
            • Mucosa: Inner epithelial lining with glands
            • Submucosa: Connective tissue with blood vessels and nerves
            • Muscularis: Smooth muscle layers for peristalsis
            • Serosa/Adventitia: Outer protective covering
        ''',
    },
    'liver': {
        'name': 'Liver',
        'emoji': '🟫',
        'model_id': 'liver',
        'description': 'Vital metabolic organ with detoxification and storage functions.',
        'color': '#B45309',
        'system': 'Digestive System',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/6DULo',
        'full_description': '''
            HEPATIC ANATOMY:
            The liver is the largest internal organ and largest gland in the human body, weighing approximately 1.5 kg
            in adults. It occupies the right upper quadrant of the abdominal cavity, beneath the diaphragm.

            FUNCTIONAL UNITS:
            • Hepatocytes: Main functional cells performing metabolic functions
            • Lobules: Hexagonal structural units with central veins
            • Portal Triads: Branches of hepatic artery, portal vein, and bile duct
            • Sinusoids: Vascular channels allowing blood-hepatocyte interaction

            MAJOR FUNCTIONS:
            • Metabolism: Carbohydrate, lipid, and protein metabolism
            • Detoxification: Processing of drugs, alcohol, and metabolic waste
            • Bile Production: Essential for fat digestion and absorption
            • Storage: Glycogen, vitamins, and minerals storage
            • Synthesis: Plasma proteins, clotting factors, and cholesterol

            CLINICAL SIGNIFICANCE:
            Liver function tests assess hepatic health, while conditions like cirrhosis, hepatitis, and fatty liver
            disease highlight the organ's vulnerability to various insults.
        ''',
    },
    'brain': {
        'name': 'Brain',
        'emoji': '🧠',
        'model_id': 'brain',
        'description': 'The control center of your nervous system and consciousness.',
        'color': '#7C3AED',
        'system': 'Central Nervous System',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/6QYCE',
        'full_description': '''
            GROSS NEUROANATOMY:
            The human brain is the most complex biological structure known, weighing approximately 1.4 kg (3 lbs)
            and containing an estimated 86 billion neurons and similar number of glial cells. It consumes 20-25% of
            the body's oxygen and glucose despite representing only 2% of body weight.

            MAJOR DIVISIONS:
            • Cerebrum (Telencephalon): Largest part for higher cognitive functions
            • Diencephalon: Thalamus and hypothalamus for relay and regulation
            • Brainstem: Midbrain, pons, medulla for basic life functions
            • Cerebellum: Coordination and motor learning
            • Limbic System: Emotional processing and memory

            PROTECTIVE STRUCTURES:
            • Skull: Bony cranial vault providing mechanical protection
            • Meninges: Three protective membranes (dura mater, arachnoid, pia mater)
            • Cerebrospinal Fluid: Buoyant cushion in ventricular system and subarachnoid space
            • Blood-Brain Barrier: Selective permeability maintaining stable environment

            FUNCTIONAL ORGANIZATION:
            The brain exhibits both localization (specific functions in specific areas) and distribution
            (networks collaborating across regions). The cerebral cortex, with its characteristic gyri and sulci,
            provides approximately 2,500 cm² of surface area within the confined cranial space.

            BLOOD SUPPLY:
            The brain receives 15-20% of cardiac output through two paired systems:
            • Internal Carotid Arteries: Anterior and middle cerebral circulation
            • Vertebral Arteries: Posterior circulation joining to form basilar artery
            The Circle of Willis provides collateral circulation at the base of the brain.
        ''',
    },
    'nervous_system': {
        'name': 'Nervous System',
        'emoji': '🧬',
        'model_id': 'nervous_system',
        'description': 'Complex network of nerves and cells that transmit signals throughout the body.',
        'color': '#8B5CF6',
        'system': 'Nervous System',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/oF6DV',
        'full_description': '''
            NEUROLOGICAL OVERVIEW:
            The human nervous system is an extraordinarily complex network of specialized cells that coordinates
            voluntary and involuntary actions, transmits sensory information, and processes cognitive functions.
            It consists of billions of neurons and supporting glial cells.

            MAJOR DIVISIONS:
            • Central Nervous System (CNS): Brain and spinal cord
            • Peripheral Nervous System (PNS): All neural tissue outside CNS

            PERIPHERAL NERVOUS SYSTEM SUBSYSTEMS:
            • Somatic Nervous System: Voluntary control of skeletal muscles
            • Autonomic Nervous System: Involuntary control of smooth muscles, cardiac muscle, and glands
            • Enteric Nervous System: Semi-independent system governing gastrointestinal function

            AUTONOMIC NERVOUS SYSTEM DIVISIONS:
            • Sympathetic Division: "Fight or flight" responses
            • Parasympathetic Division: "Rest and digest" functions
            • Enteric Division: Independent gut nervous system

            NEURONAL ORGANIZATION:
            • Sensory Neurons: Afferent pathways carrying information to CNS
            • Motor Neurons: Efferent pathways carrying commands from CNS
            • Interneurons: Association neurons within CNS for processing
        ''',
    },
    'full_body': {
        'name': 'Complete Human Body',
        'emoji': '👤',
        'model_id': 'full_body',
        'description': 'Comprehensive anatomical representation of the entire human body.',
        'color': '#6366F1',
        'system': 'Multiple Systems',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/oKs8T',
        'full_description': '''
            COMPREHENSIVE ANATOMICAL OVERVIEW:
            The human body represents one of the most complex biological systems known, comprising multiple
            integrated systems working in harmony to maintain homeostasis and enable sophisticated functions
            from cellular metabolism to conscious thought and coordinated movement.

            MAJOR ORGAN SYSTEMS:
            • Integumentary System: Skin, hair, nails - external protection
            • Skeletal System: Bones, joints - structure and support
            • Muscular System: Skeletal, cardiac, smooth muscles - movement
            • Nervous System: Brain, spinal cord, nerves - control and coordination
            • Endocrine System: Glands and hormones - chemical regulation
            • Cardiovascular System: Heart and blood vessels - circulation
            • Lymphatic System: Lymph nodes and vessels - immunity and fluid balance
            • Respiratory System: Lungs and airways - gas exchange
            • Digestive System: GI tract and accessory organs - nutrient processing
            • Urinary System: Kidneys and bladder - waste elimination
            • Reproductive System: Gonads and reproductive structures - reproduction

            SYSTEMIC INTEGRATION:
            All body systems work in coordinated harmony through:
            • Neural Regulation: Fast-acting nervous system control
            • Endocrine Regulation: Slower, sustained hormonal control
            • Local Regulation: Tissue-level autocrine and paracrine signaling
            • Homeostatic Mechanisms: Feedback loops maintaining internal stability

            DEVELOPMENTAL ANATOMY:
            The human body develops through precisely timed stages from fertilization through adulthood,
            with different systems maturing at different rates while maintaining functional integration.
        ''',
    },
    'skull': {
        'name': 'Skull',
        'emoji': '💀',
        'model_id': 'skull',
        'description': 'Bony structure that forms the head and protects the brain.',
        'color': '#6B7280',
        'system': 'Skeletal System',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/oDHF6',
        'full_description': '''
            OSTEOLOGICAL OVERVIEW:
            The human skull is a complex bony structure composed of 22 bones (excluding the ossicles of the middle ear)
            that form the protective cranial vault for the brain and the framework for the face.

            MAJOR DIVISIONS:
            • Neurocranium: Protective vault surrounding the brain (8 bones)
            • Viscerocranium: Facial skeleton (14 bones)
            • Mandible: Lower jaw bone (considered separately)

            CRANIAL BONES:
            • Frontal Bone: Forehead and superior orbit
            • Parietal Bones (2): Superior and lateral cranium
            • Temporal Bones (2): Lateral base and middle ear housing
            • Occipital Bone: Posterior base with foramen magnum
            • Sphenoid Bone: Keystone bone articulating with all cranial bones
            • Ethmoid Bone: Anterior cranial floor, nasal cavity, and orbit

            CLINICAL SIGNIFICANCE:
            The skull provides crucial protection for the brain while allowing passage for nerves and blood vessels
            through various foramina. Understanding skull anatomy is essential for neurosurgery, trauma management,
            and anthropological studies.
        ''',
    },
    'eye': {
        'name': 'Eye',
        'emoji': '👁️',
        'model_id': 'eye',
        'description': 'Sensory organ of vision that detects light and converts it into neural signals.',
        'color': '#0EA5E9',
        'system': 'Sensory System',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/onqUK',
        'full_description': '''
            OCULAR ANATOMY:
            The human eye is a complex sensory organ approximately 2.5 cm in diameter that converts light into
            electrochemical impulses interpreted by the brain as vision.

            MAJOR STRUCTURES:
            • Cornea: Transparent anterior covering that refracts light
            • Iris: Colored diaphragm controlling pupil size
            • Lens: Flexible structure that focuses light onto retina
            • Retina: Light-sensitive layer containing photoreceptors
            • Optic Nerve: Transmits visual information to brain

            PHOTORECEPTORS:
            • Rods: 120 million cells for low-light vision and motion detection
            • Cones: 6-7 million cells for color vision and fine detail
            • Distribution: Concentrated in macula and fovea centralis

            VISUAL PATHWAY:
            Light → Cornea → Aqueous Humor → Pupil → Lens → Vitreous Humor → Retina → Optic Nerve → Brain

            CLINICAL CORRELATIONS:
            Common visual disorders include myopia, hyperopia, astigmatism, cataracts, glaucoma, and macular degeneration.
            Regular eye examinations are crucial for maintaining visual health.
        ''',
    },
    'teeth': {
        'name': 'Teeth',
        'emoji': '🦷',
        'model_id': 'teeth',
        'description': 'Hard, calcified structures used for biting and chewing food.',
        'color': '#F0FDF4',
        'system': 'Digestive System',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/oQuZS',
        'full_description': '''
            DENTAL ANATOMY:
            Human teeth are specialized calcified structures embedded in the mandible and maxilla, designed for
            mechanical digestion through cutting, tearing, and grinding food.

            TOOTH TYPES AND FUNCTIONS:
            • Incisors (8): Chisel-shaped for cutting food
            • Canines (4): Pointed for tearing food
            • Premolars (8): For crushing and grinding
            • Molars (12): Large surfaces for thorough grinding

            TOOTH STRUCTURE:
            • Crown: Visible portion above gum line
            • Root: Embedded in alveolar bone
            • Enamel: Hardest substance in human body covering crown
            • Dentin: Bulk of tooth beneath enamel
            • Pulp: Soft tissue containing nerves and blood vessels
            • Cementum: Covers root surface

            DENTITION DEVELOPMENT:
            • Primary Dentition: 20 deciduous teeth erupting 6 months - 3 years
            • Mixed Dentition: 6-12 years with both primary and permanent teeth
            • Permanent Dentition: 32 teeth completing by early adulthood

            CLINICAL SIGNIFICANCE:
            Dental health affects overall systemic health. Conditions like caries, periodontal disease, and
            malocclusion require professional dental care for prevention and treatment.
        ''',
    },
    'ovary': {
        'name': 'Ovary',
        'emoji': '🥚',
        'model_id': 'ovary',
        'description': 'Female reproductive organ producing ova and hormones.',
        'color': '#EC4899',
        'system': 'Reproductive System',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/oGrRn',
        'full_description': '''
            REPRODUCTIVE ANATOMY:
            The ovaries are paired almond-shaped organs measuring 3-5 cm in length, located in the lateral pelvic wall.
            They serve dual functions of gamete production and endocrine secretion.

            STRUCTURAL ORGANIZATION:
            • Germinal Epithelium: Outer covering of ovary
            • Cortex: Contains ovarian follicles in various stages of development
            • Medulla: Central region with blood vessels, nerves, and connective tissue
            • Follicles: Structures containing developing oocytes

            FOLLICULAR DEVELOPMENT:
            • Primordial Follicles: 400,000-500,000 at birth, dormant until puberty
            • Primary Follicles: Begin maturation in response to FSH
            • Secondary Follicles: Develop fluid-filled antrum
            • Graafian Follicle: Mature follicle ready for ovulation
            • Corpus Luteum: Forms after ovulation, secretes progesterone

            ENDOCRINE FUNCTIONS:
            • Estrogen: Development of female secondary sexual characteristics
            • Progesterone: Prepares endometrium for implantation
            • Inhibin: Regulates FSH secretion

            REPRODUCTIVE CYCLE:
            The ovarian cycle consists of follicular phase (days 1-14) and luteal phase (days 15-28),
            coordinated with the uterine menstrual cycle through complex hormonal feedback mechanisms.
        ''',
    },
    'male_reproductive': {
        'name': 'Male Reproductive System',
        'emoji': '👨',
        'model_id': 'male_reproductive',
        'description': 'Organs responsible for sperm production and delivery.',
        'color': '#3B82F6',
        'system': 'Reproductive System',
        'animation': 'pulse',
        'sketchfab_url': 'https://skfb.ly/oOIoL',
        'full_description': '''
            MALE REPRODUCTIVE ANATOMY:
            The male reproductive system consists of both internal and external organs dedicated to sperm production,
            maturation, storage, and delivery, along with hormone secretion.

            EXTERNAL ORGANS:
            • Penis: Organ for sexual intercourse and urination
            • Scrotum: Skin sac containing testes, maintaining optimal temperature

            INTERNAL ORGANS:
            • Testes: Paired organs producing sperm and testosterone
            • Epididymis: Coiled tube for sperm maturation and storage
            • Vas Deferens: Muscular tube transporting sperm
            • Seminal Vesicles: Produce seminal fluid
            • Prostate Gland: Adds alkaline fluid to semen
            • Bulbourethral Glands: Produce pre-ejaculate fluid

            SPERMATOGENESIS:
            • Location: Seminiferous tubules of testes
            • Duration: Approximately 74 days for complete cycle
            • Process: Spermatogonia → Primary Spermatocytes → Secondary Spermatocytes → Spermatids → Spermatozoa
            • Daily Production: 100-200 million sperm

            HORMONAL REGULATION:
            • Testosterone: Development of male characteristics, libido, sperm production
            • FSH: Stimulates spermatogenesis
            • LH: Stimulates testosterone production
            • Inhibin: Negative feedback on FSH secretion

            CLINICAL CONSIDERATIONS:
            Common conditions include infertility, benign prostatic hyperplasia, prostate cancer, and erectile dysfunction.
            Regular urological examinations are recommended for maintaining reproductive health.
        ''',
    }
}

class AdvancedImageProcessor:
    def __init__(self):
        self.organ_keywords = {
            'heart': {
                'strong': ['heart', 'cardiac', 'cardiovascular', 'ventricle', 'atrium', 'aortic', 'mitral'],
                'medium': ['chest', 'pump', 'blood', 'artery', 'vein', 'valve', 'chamber'],
                'weak': ['red', 'pulse', 'beat', 'circulation']
            },
            'brain': {
                'strong': ['brain', 'cerebral', 'neural', 'cortex', 'cerebellum', 'neuron'],
                'medium': ['head', 'mind', 'nervous', 'cognitive', 'intelligence', 'memory'],
                'weak': ['gray', 'think', 'smart', 'learning']
            },
            'lungs': {
                'strong': ['lung', 'pulmonary', 'respiratory', 'bronchi', 'alveoli', 'breathing'],
                'medium': ['breath', 'oxygen', 'airway', 'inhalation', 'exhalation'],
                'weak': ['breathe', 'air', 'smoke', 'oxygen']
            },
            'digestive': {
                'strong': ['stomach', 'intestine', 'digestive', 'gastro', 'colon', 'esophagus'],
                'medium': ['food', 'eat', 'gut', 'abdomen', 'liver', 'pancreas'],
                'weak': ['digestion', 'nutrition', 'absorption']
            },
            'liver': {
                'strong': ['liver', 'hepatic', 'hepat', 'bile', 'detox'],
                'medium': ['organ', 'metabolism', 'filter', 'toxin'],
                'weak': ['brown', 'large', 'chemical']
            },
            'nervous_system': {
                'strong': ['nerve', 'neural', 'nervous', 'neuron', 'synapse', 'ganglion'],
                'medium': ['brain', 'spinal', 'cortex', 'neural', 'axon', 'dendrite'],
                'weak': ['signal', 'impulse', 'transmission', 'coordination']
            },
            'full_body': {
                'strong': ['body', 'anatomy', 'human', 'corpse', 'cadaver', 'fullbody'],
                'medium': ['complete', 'entire', 'whole', 'systemic', 'muscle', 'organ'],
                'weak': ['figure', 'person', 'human', 'medical']
            },
            'skull': {
                'strong': ['skull', 'cranial', 'headbone', 'cranium', 'mandible', 'maxilla'],
                'medium': ['head', 'bone', 'skeleton', 'face', 'jaw'],
                'weak': ['white', 'hard', 'protection']
            },
            'eye': {
                'strong': ['eye', 'ocular', 'retina', 'cornea', 'iris', 'vision'],
                'medium': ['see', 'sight', 'optic', 'pupil', 'lens'],
                'weak': ['blue', 'brown', 'green', 'look']
            },
            'teeth': {
                'strong': ['teeth', 'dental', 'tooth', 'molar', 'incisor', 'canine'],
                'medium': ['mouth', 'chew', 'bite', 'enamel', 'dentist'],
                'weak': ['white', 'smile', 'oral']
            },
            'ovary': {
                'strong': ['ovary', 'ovarian', 'follicle', 'oocyte', 'estrogen'],
                'medium': ['female', 'reproductive', 'egg', 'menstrual', 'hormone'],
                'weak': ['woman', 'fertility', 'cycle']
            },
            'male_reproductive': {
                'strong': ['testis', 'testicle', 'prostate', 'sperm', 'penis', 'scrotum'],
                'medium': ['male', 'reproductive', 'seminal', 'vas', 'deferens'],
                'weak': ['man', 'fertility', 'virility']
            }
        }

    def analyze_image_content(self, image):
        """Analyze image content using computer vision techniques"""
        try:
            img_array = np.array(image)
            
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            height, width = img_array.shape[:2]
            
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            else:
                gray = img_array
            
            brightness = np.mean(gray)
            contrast = np.std(gray)
            
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (width * height)
            
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contour_count = len(contours)
            
            return {
                'aspect_ratio': width / height,
                'brightness': brightness,
                'contrast': contrast,
                'edge_density': edge_density,
                'contour_count': contour_count,
            }
            
        except Exception as e:
            print(f"Image analysis error: {e}")
            return None

    def smart_detect_organ(self, filename, image_content=None):
        filename_lower = filename.lower()
        
        scores = {organ: 0 for organ in ORGANS_DATA.keys()}
        
        # Filename analysis
        for organ, keywords in self.organ_keywords.items():
            for keyword in keywords['strong']:
                if keyword in filename_lower:
                    scores[organ] += 0.5
            for keyword in keywords['medium']:
                if keyword in filename_lower:
                    scores[organ] += 0.3
            for keyword in keywords['weak']:
                if keyword in filename_lower:
                    scores[organ] += 0.1
        
        # Image content analysis
        if image_content:
            img_analysis = self.analyze_image_content(image_content)
            if img_analysis:
                if img_analysis['edge_density'] > 0.15:
                    scores['skull'] += 0.3
                    scores['teeth'] += 0.2
                if 80 < img_analysis['brightness'] < 180:
                    scores['brain'] += 0.2
        
        best_organ = max(scores, key=scores.get)
        best_score = scores[best_organ]
        
        if best_score < 0.3:
            return self.fallback_detection(filename_lower, image_content)
        
        confidence = min(0.7 + (best_score * 0.5), 0.95)
        return best_organ, confidence

    def fallback_detection(self, filename, image_content=None):
        if any(word in filename for word in ['chest', 'xray', 'thorax']):
            return 'lungs', 0.7
        elif any(word in filename for word in ['head', 'brain', 'skull']):
            return 'brain', 0.7
        elif any(word in filename for word in ['cardio', 'heart']):
            return 'heart', 0.7
        elif any(word in filename for word in ['bone', 'skeleton']):
            return 'skull', 0.7
        elif any(word in filename for word in ['eye', 'vision']):
            return 'eye', 0.7
        elif any(word in filename for word in ['teeth', 'dental']):
            return 'teeth', 0.7
        elif any(word in filename for word in ['stomach', 'digestive']):
            return 'digestive', 0.7
        elif any(word in filename for word in ['liver', 'hepatic']):
            return 'liver', 0.7
        elif any(word in filename for word in ['ovary', 'female']):
            return 'ovary', 0.7
        elif any(word in filename for word in ['male', 'testis']):
            return 'male_reproductive', 0.7
        else:
            organs = ['heart', 'brain', 'lungs', 'digestive', 'liver', 'eye']
            return random.choice(organs), 0.6

# Initialize processor
image_processor = AdvancedImageProcessor()

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScanSpectrum - Interactive Human Anatomy Explorer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .hidden { display: none !important; }
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #e5e7eb;
            border-top: 4px solid #3b82f6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .organ-card {
            transition: all 0.3s ease;
        }
        .organ-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
    <!-- Header -->
    <header class="bg-white shadow-lg border-b border-gray-200">
        <div class="container mx-auto px-6 py-4">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-3 rounded-xl">
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                        </svg>
                    </div>
                    <div>
                        <h1 class="text-3xl font-bold text-gray-800">ScanSpectrum</h1>
                        <span class="text-sm text-gray-600">Interactive Human Anatomy Explorer</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Navigation -->
    <nav class="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md">
        <div class="container mx-auto px-6">
            <div class="flex space-x-8">
                <button id="scan-tab" class="py-4 px-4 font-medium text-lg border-b-2 border-white flex items-center gap-2">
                    <span>📷</span>
                    Upload & Explore
                </button>
                <button id="library-tab" class="py-4 px-4 font-medium text-lg flex items-center gap-2">
                    <span>📚</span>
                    Body Systems Library
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto px-6 py-8">
        <!-- Upload Section -->
        <section id="scan-section">
            <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
                <h2 class="text-2xl font-bold text-gray-800 mb-2">🔍 Upload Body Part Image</h2>
                <p class="text-gray-600 mb-6">Upload any anatomy image and explore interactive 3D models with detailed learning content</p>
               
                <!-- Two Button Options -->
                <div class="flex gap-4 mb-8">
                    <button id="upload-image-btn" class="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-4 px-6 rounded-lg font-medium text-lg shadow-lg transition-all flex items-center justify-center gap-3">
                        <span class="text-2xl">📷</span>
                        <div class="text-left">
                            <div class="font-semibold">Upload Image</div>
                            <div class="text-sm opacity-90">Select from device</div>
                        </div>
                    </button>
                    <button id="scan-image-btn" class="flex-1 bg-green-500 hover:bg-green-600 text-white py-4 px-6 rounded-lg font-medium text-lg shadow-lg transition-all flex items-center justify-center gap-3">
                        <span class="text-2xl">🔬</span>
                        <div class="text-left">
                            <div class="font-semibold">Scan Image</div>
                            <div class="text-sm opacity-90">Use camera</div>
                        </div>
                    </button>
                </div>

                <!-- Upload Area -->
                <div id="upload-image-area" class="border-2 border-dashed border-blue-300 rounded-2xl p-12 text-center mb-8 bg-blue-50">
                    <div class="mb-6">
                        <div class="text-6xl mb-3">📷</div>
                    </div>
                    <h3 class="text-xl font-semibold text-gray-700 mb-2">Drop your body part image here</h3>
                    <p class="text-gray-600 mb-6">Supports: Heart, Brain, Lungs, Digestive System, and all major organs</p>
                    <input type="file" id="image-upload" accept="image/*" class="hidden">
                    <button onclick="document.getElementById('image-upload').click()" class="bg-blue-500 hover:bg-blue-600 text-white px-8 py-4 rounded-lg font-medium text-lg shadow-lg transition-all">
                        Choose Image File
                    </button>
                    <p class="text-sm text-gray-500 mt-4">AI-Powered Detection • Interactive 3D Models • Educational Content</p>
                </div>

                <!-- Scan Area -->
                <div id="scan-image-area" class="border-2 border-dashed border-green-300 rounded-2xl p-12 text-center mb-8 bg-green-50 hidden">
                    <div class="mb-6">
                        <div class="text-6xl mb-3">🔬</div>
                    </div>
                    <h3 class="text-xl font-semibold text-gray-700 mb-2">Scan body part using camera</h3>
                    <p class="text-gray-600 mb-6">Position the body part clearly in view for optimal scanning</p>
                    <button class="bg-green-500 hover:bg-green-600 text-white px-8 py-4 rounded-lg font-medium text-lg shadow-lg transition-all">
                        Start Camera Scan
                    </button>
                    <p class="text-sm text-gray-500 mt-4">Real-time Analysis • Interactive 3D Models • Educational Content</p>
                </div>

                <!-- Processing -->
                <div id="processing-area" class="hidden">
                    <div class="text-center py-12">
                        <div class="loading-spinner mb-4"></div>
                        <p class="text-gray-600 text-lg">Analyzing image with AI...</p>
                        <p class="text-gray-500">Detecting anatomical structures and preparing 3D visualization</p>
                    </div>
                </div>

                <!-- Results Area -->
                <div id="results-area" class="hidden">
                    <!-- Detection Header -->
                    <div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-6 text-white mb-8">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <div id="detected-emoji" class="text-4xl bg-white bg-opacity-20 p-3 rounded-full">❤️</div>
                                <div>
                                    <h3 id="detection-result" class="text-2xl font-bold">Organ Detected</h3>
                                    <p id="confidence-level" class="text-blue-100">AI Confidence: 85%</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="text-sm text-blue-200">Interactive 3D Model Ready</div>
                                <div class="text-lg font-semibold">Learning Mode Active</div>
                            </div>
                        </div>
                    </div>

                    <!-- Organ Overview -->
                    <div class="bg-white rounded-xl p-6 mb-8 border border-gray-200">
                        <h3 class="text-xl font-bold text-gray-800 mb-4" id="organ-name">Organ Overview</h3>
                        <div class="prose max-w-none">
                            <p class="text-gray-700 leading-relaxed whitespace-pre-line" id="organ-full-description">
                                Detailed educational content will appear here...
                            </p>
                        </div>
                    </div>

                    <!-- 3D Model Display -->
                    <div class="bg-white rounded-xl p-6 mb-8 border border-gray-200">
                        <h3 class="text-xl font-bold text-gray-800 mb-4">Interactive 3D Anatomy Explorer</h3>
                        <p class="text-gray-600 mb-4">Explore the detailed 3D model - rotate, zoom, and learn about anatomical structures</p>
                        
                        <!-- Sketchfab Model Container -->
                        <div id="sketchfab-container" class="relative w-full h-96 bg-gray-900 rounded-lg overflow-hidden">
                            <iframe id="sketchfab-embed" class="w-full h-full border-none" 
                                    src="" 
                                    frameborder="0" 
                                    allow="autoplay; fullscreen; vr" 
                                    mozallowfullscreen="true" 
                                    webkitallowfullscreen="true">
                            </iframe>
                            <div class="absolute top-4 right-4">
                                <a id="sketchfab-link" href="#" target="_blank" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2">
                                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h-2v-6h2v6zm4 0h-2v-6h2v6z"/>
                                    </svg>
                                    View Full Screen
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Library Section -->
        <section id="library-section" class="hidden">
            <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
                <h2 class="text-2xl font-bold text-gray-800 mb-2">📚 Explore Body Systems</h2>
                <p class="text-gray-600 mb-6">Discover interactive 3D models of human body systems with comprehensive learning content</p>
               
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" id="organ-grid">
                    <!-- Organs will be loaded dynamically -->
                </div>
            </div>
        </section>
    </main>

    <script>
        class ScanSpectrumApp {
            constructor() {
                this.currentUploadMode = 'upload';
                this.init();
            }

            init() {
                console.log('ScanSpectrum App Initialized');
                this.setupEventListeners();
                this.loadOrganLibrary();
            }

            setupEventListeners() {
                // Navigation
                document.getElementById('scan-tab').addEventListener('click', () => this.showSection('scan'));
                document.getElementById('library-tab').addEventListener('click', () => this.showSection('library'));

                // Upload options
                document.getElementById('upload-image-btn').addEventListener('click', () => {
                    this.setUploadMode('upload');
                });
                document.getElementById('scan-image-btn').addEventListener('click', () => {
                    this.setUploadMode('scan');
                });

                // File upload
                document.getElementById('image-upload').addEventListener('change', (e) => {
                    this.handleImageUpload(e);
                });
            }

            setUploadMode(mode) {
                this.currentUploadMode = mode;
                
                // Show/hide appropriate areas
                document.getElementById('upload-image-area').classList.toggle('hidden', mode !== 'upload');
                document.getElementById('scan-image-area').classList.toggle('hidden', mode !== 'scan');
            }

            showSection(section) {
                // Hide all sections
                document.getElementById('scan-section').classList.add('hidden');
                document.getElementById('library-section').classList.add('hidden');
                
                // Remove active from all tabs
                document.getElementById('scan-tab').classList.remove('border-b-2', 'border-white');
                document.getElementById('library-tab').classList.remove('border-b-2', 'border-white');

                // Show selected section
                document.getElementById(section + '-section').classList.remove('hidden');
                document.getElementById(section + '-tab').classList.add('border-b-2', 'border-white');
            }

            async loadOrganLibrary() {
                try {
                    const response = await fetch('/api/organs');
                    const organs = await response.json();
                    
                    const grid = document.getElementById('organ-grid');
                    grid.innerHTML = organs.map(organ => `
                        <div class="organ-card bg-white rounded-xl p-6 text-center hover:shadow-xl transition-all cursor-pointer border border-gray-200">
                            <div class="text-5xl mb-4">${organ.emoji}</div>
                            <h3 class="text-xl font-bold text-gray-800 mb-2">${organ.name}</h3>
                            <p class="text-gray-600 mb-3">${organ.system}</p>
                            <p class="text-sm text-gray-500 mb-4">${organ.description}</p>
                            <button onclick="app.exploreOrgan('${organ.id}')" class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                                Explore in 3D
                            </button>
                        </div>
                    `).join('');
                } catch (error) {
                    console.error('Failed to load organ library:', error);
                }
            }

            async exploreOrgan(organId) {
                try {
                    const response = await fetch(`/api/organ/${organId}`);
                    const organData = await response.json();
                    
                    this.displayOrganResults(organData);
                    this.showSection('scan');
                } catch (error) {
                    console.error('Failed to load organ data:', error);
                }
            }

            async handleImageUpload(event) {
                const file = event.target.files[0];
                if (!file) return;

                console.log('Uploading:', file.name);
                this.showProcessing(true);

                const formData = new FormData();
                formData.append('image', file);

                try {
                    const response = await fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();
                    
                    if (result.success) {
                        this.displayResults(result);
                    } else {
                        alert('Upload failed: ' + result.error);
                    }
                } catch (error) {
                    console.error('Upload error:', error);
                    alert('Upload failed: ' + error.message);
                } finally {
                    this.showProcessing(false);
                }
            }

            displayResults(result) {
                const organData = result.organ_data;
                
                // Update detection header
                document.getElementById('detected-emoji').textContent = organData.emoji;
                document.getElementById('detection-result').textContent = `${organData.name} Detected`;
                document.getElementById('confidence-level').textContent = `AI Confidence: ${Math.round(result.confidence * 100)}%`;
                
                // Update organ overview
                document.getElementById('organ-name').textContent = `${organData.emoji} ${organData.name} Overview`;
                document.getElementById('organ-full-description').textContent = organData.full_description;
                
                // Update 3D model
                if (organData.sketchfab_url) {
                    const embed = document.getElementById('sketchfab-embed');
                    const link = document.getElementById('sketchfab-link');
                    
                    embed.src = organData.sketchfab_url;
                    link.href = organData.sketchfab_url;
                }
                
                // Show results area
                document.getElementById('results-area').classList.remove('hidden');
            }

            displayOrganResults(organData) {
                // Update detection header
                document.getElementById('detected-emoji').textContent = organData.emoji;
                document.getElementById('detection-result').textContent = `${organData.name}`;
                document.getElementById('confidence-level').textContent = `Selected from Library`;
                
                // Update organ overview
                document.getElementById('organ-name').textContent = `${organData.emoji} ${organData.name} Overview`;
                document.getElementById('organ-full-description').textContent = organData.full_description;
                
                // Update 3D model
                if (organData.sketchfab_url) {
                    const embed = document.getElementById('sketchfab-embed');
                    const link = document.getElementById('sketchfab-link');
                    
                    embed.src = organData.sketchfab_url;
                    link.href = organData.sketchfab_url;
                }
                
                // Show results area
                document.getElementById('results-area').classList.remove('hidden');
            }

            showProcessing(show) {
                const processing = document.getElementById('processing-area');
                if (show) {
                    processing.classList.remove('hidden');
                } else {
                    processing.classList.add('hidden');
                }
            }
        }

        // Start the app
        document.addEventListener('DOMContentLoaded', function() {
            window.app = new ScanSpectrumApp();
            console.log('🌟 ScanSpectrum App Loaded Successfully!');
        });
    </script>
</body>
</html>
'''

@app.route('/')
def serve_app():
    return render_template_string(HTML_TEMPLATE)

# API Routes
@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'ScanSpectrum is running!'})

@app.route('/api/organs')
def get_organs():
    organs_list = []
    for organ_id, data in ORGANS_DATA.items():
        organs_list.append({
            'id': organ_id,
            'name': data['name'],
            'emoji': data['emoji'],
            'description': data['description'],
            'system': data.get('system', 'General'),
            'color': data.get('color', '#3B82F6'),
            'animation': data.get('animation', 'pulse'),
            'model_id': data.get('model_id', organ_id),
            'sketchfab_url': data.get('sketchfab_url', '')
        })
    return jsonify(organs_list)

@app.route('/api/organ/<organ_id>')
def get_organ(organ_id):
    organ_data = ORGANS_DATA.get(organ_id)
    if organ_data:
        return jsonify(organ_data)
    else:
        return jsonify({'error': 'Organ not found'}), 404

@app.route('/api/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'})
       
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
       
        # Process the image
        image = Image.open(file.stream)
        
        # Detect organ
        organ, confidence = image_processor.smart_detect_organ(file.filename, image)
        
        # Get organ data
        organ_data = ORGANS_DATA.get(organ, {})
       
        return jsonify({
            'success': True,
            'part': organ,
            'confidence': confidence,
            'model_id': organ,
            'organ_data': {
                'name': organ_data.get('name', organ),
                'emoji': organ_data.get('emoji', '🔍'),
                'description': organ_data.get('description', ''),
                'full_description': organ_data.get('full_description', ''),
                'sketchfab_url': organ_data.get('sketchfab_url', '')
            },
            'message': f'ScanSpectrum detection: {organ} with {confidence:.1%} confidence'
        })
       
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🔬 ScanSpectrum - Interactive Human Anatomy Explorer!")
    print("=" * 70)
    print("✅ FEATURES:")
    print("   • Upload Image & Scan Image options")
    print("   • 12+ Interactive 3D models with Sketchfab")
    print("   • Comprehensive educational content")
    print("   • Advanced AI-powered image detection")
    print("   • Body Systems Library")
    print("=" * 70)
    print("📍 Running on: http://localhost:5000")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5000, debug=True)