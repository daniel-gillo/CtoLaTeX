/* Should work. */
void main(int i) {
	if (i == 1) {
		i = i + 1;
		if (i == -2) {
			i = i + 5;
			if (i == 2) {
				i = -1;
			} 
		} else {
			i = -2;
		}
	} else {
		i = i - 1;
	}
}