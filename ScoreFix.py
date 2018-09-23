def scoreFix (score, scale, sum):
	scoreType = (type(score) == int) or (type(score) == float)
	scaleType = (type(scale) == int) or (type(scale) == float)
	sumType = (type(sum) == int) or (type(sum) == float)
	
	allNumBool = scoreType and scaleType and sumType
	
	if allNumBool:
		scoreGTScale = score > scale
		
		if scoreGTScale:
			return "Your score exceeds your scale.  Try again.  "
		else:
			for a in range(5):
				scale = scale
				score = score
				sumNum = sum
				
				scaleHund = (100/scale)
				
				scoreHund = score * scaleHund
				scaleHund = scale * scaleHund
				
				prcnt = (scoreHund / scaleHund) * 100
				
				scoreDiv = prcnt * sumNum
				
				return scoreDiv
	

print(scoreFix(1, 2, 9))
print(scoreFix(12.3, 2, 3))
print(scoreFix("a", 2, 3))
print(scoreFix("0", 1, 1.2))
