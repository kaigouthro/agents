from abc import abstractmethod


class PromptComponent:
    def __init__(self):
        pass

    @abstractmethod
    def get_prompt(self, agent):
        pass

class TaskComponent(PromptComponent):
    def __init__(self, task):
        super().__init__()
        self.task = task

    def get_prompt(self, agent):
        return f"""The task you need to execute is: <task>{self.task}</task>.\n"""


class OutputComponent(PromptComponent):
    def __init__(self, output):
        super().__init__()
        self.output = output

    def get_prompt(self, agent):
        return f"""Please contact the above to extract <{self.output}> and </{self.output}>, \
            do not perform additional output, please output in strict accordance with the above format!\n"""


class SystemComponent(PromptComponent):
    def __init__(self,system_prompt):
        super().__init__()
        self.system_prompt = system_prompt
    
    def get_prompt(self, agent):
        return self.system_prompt

class LastComponent(PromptComponent):
    def __init__(self, last_prompt):
        super().__init__()
        self.last_prompt = last_prompt

    def get_prompt(self, agent):
        return self.last_prompt


class StyleComponent(PromptComponent):
    """
    角色、风格组件
    """

    def __init__(self, role):
        super().__init__()
        self.role = role

    def get_prompt(self, agent):
        name = agent.name
        style = agent.style
        return f"""Now your role is:\n<role>{self.role}</role>, your name is:\n<name>{name}</name>. \
            You need to follow the output style:\n<style>{style}</style>.\n"""


class RuleComponent(PromptComponent):
    def __init__(self, rule):
        super().__init__()
        self.rule = rule

    def get_prompt(self, agent):
        return f"""The rule you need to follow is:\n<rule>{self.rule}</rule>.\n"""


class DemonstrationComponent(PromptComponent):
    """
    input a list,the example of answer.
    """

    def __init__(self, demonstrations):
        super().__init__()
        self.demonstrations = demonstrations

    def add_demonstration(self, demonstration):
        self.demonstrations.append(demonstration)

    def get_prompt(self, agent):
        prompt = "Here are demonstrations you can refer to:\n<demonstrations>"
        for demonstration in self.demonstrations:
            prompt += "\n" + demonstration
        prompt += "</demonstrations>\n"
        return prompt


class CoTComponent(PromptComponent):
    """
    input a list,the example of answer.
    """

    def __init__(self, demonstrations):
        super().__init__()
        self.demonstrations = demonstrations

    def add_demonstration(self, demonstration):
        self.demonstrations.append(demonstration)

    def get_prompt(self, agent):
        prompt = "You need to think in detail before outputting, the thinking case is as follows:\n<demonstrations>"
        for demonstration in self.demonstrations:
            prompt += "\n" + demonstration
        prompt += "</demonstrations>\n"
        return prompt


class CustomizeComponent(PromptComponent):
    """
    Custom template
    template(str) : example: "i am {}"
    keywords(list) : example : ["name"]  
    example : agent.environment.shared_memory["name"] = "Lilong"
    the component will get the keyword attribute from the environment, and then add it to the template.
    Return : "i am Lilong"
    """
    def __init__(self, template, keywords) -> None:
        super().__init__()
        self.template = template
        self.keywords = keywords

    def get_prompt(self, agent):
        template_keyword = {
            keyword: agent.environment.shared_memory[keyword]
            for keyword in self.keywords
        }
        return self.template.format(**template_keyword)