from rete.common import Token, BetaNode, DEBUG


class NegativeJoinResult:

	def __init__(self, owner, wme):
		"""
		:type wme: rete.WME
		:type owner: rete.Token
		"""
		self.owner = owner
		self.wme = wme

	def __repr__(self):
		return "NJR:" + repr(self.owner) + ":" + repr(self.wme)

class NegativeNode(BetaNode):

	def __init__(self, children=None, parent=None, amem=None, tests=None):
		"""
		:type amem: rete.alpha.AlphaMemory
		"""
		super(NegativeNode, self).__init__(children=children, parent=parent)
		self.items = []			# list of tokens
		self.amem = amem
		self.tests = tests if tests else []

	def left_activation(self, token, wme, binding=None):
		"""
		:type wme: rete.WME
		:type token: rete.Token
		:type binding: dict
		"""
		DEBUG("Neg node left-activate, wme = ", wme)
		new_token = Token(token, wme, self, binding)
		self.items.append(new_token)
		for item in self.amem.items:
			if self.perform_join_test(new_token, item):
				jr = NegativeJoinResult(new_token, item)
				new_token.join_results.append(jr)
				item.negative_join_results.append(jr)
		if not new_token.join_results:			# join results == []
			for child in self.children:
				child.left_activation(new_token, None)

	def right_activation(self, wme):
		"""
		:type wme: rete.WME
		"""
		DEBUG("Neg node right-activate, wme = ", wme)
		for tok in self.items:
			if self.perform_join_test(tok, wme):
				# If join_results changes from 0 --> 1, this means the negative node is
				# previously satisfied but now unsatisfied (ie, non-negative).  Then this
				# token should not propagate further down, its descendents should be removed.
				if not tok.join_results:
					Token.delete_descendents_of_token(tok)
				jr = NegativeJoinResult(tok, wme)
				tok.join_results.append(jr)
				wme.negative_join_results.append(jr)

	def perform_join_test(self, token, wme):
		"""
		:type token: rete.Token
		:type wme: rete.WME
		"""
		for this_test in self.tests:
			arg1 = getattr(wme, this_test.field_of_arg1)
			wme2 = token.wmes[this_test.condition_number_of_arg2]
			arg2 = getattr(wme2, this_test.field_of_arg2)
			if arg1 != arg2:
				return False
		return True
