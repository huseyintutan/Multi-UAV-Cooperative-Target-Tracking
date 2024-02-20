$input v_texcoord0

#include <bgfx_shader.sh>

uniform vec4 color;
SAMPLER2D(s_tex, 0);

void main() {
	gl_FragColor = texture2D(s_tex, v_texcoord0) * color;
}
